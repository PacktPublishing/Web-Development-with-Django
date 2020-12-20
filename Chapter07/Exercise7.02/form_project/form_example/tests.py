import re
from unittest import mock

from django.http import HttpRequest, QueryDict
from django.test import Client
from django.test import TestCase

from form_example.forms import OrderForm
from form_example.views import form_example


class Exercise2Test(TestCase):
    def test_fields_in_view(self):
        """"
        Test that some fields exist in the rendered template, assume that if all the fields exist on the form class
        (there is a separate test for this) then they will all be rendered. There's no reason why only some would be.
        """
        c = Client()
        response = c.get('/form-example/')

        self.assertIsNotNone(re.search(r'<input type="hidden" name="csrfmiddlewaretoken" value="\w+">',
                                       response.content.decode('ascii')))

        self.assertIn(b'<p><label for="id_magazine_count">Magazine count:</label> <input type="number" '
                      b'name="magazine_count" placeholder="Number of Magazines" min="0" max="80" required '
                      b'id="id_magazine_count"></p>', response.content)
        self.assertIn(b'<p><label for="id_book_count">Book count:</label> <input type="number" name="book_count" '
                      b'placeholder="Number of Books" min="0" max="50" required id="id_book_count"></p>',
                      response.content)
        self.assertIn(b'<p><label for="id_send_confirmation">Send confirmation:</label> <input type="checkbox" '
                      b'name="send_confirmation" id="id_send_confirmation"></p>', response.content)
        self.assertIn(
            b'<p><label for="id_email">Email:</label> <input type="email" name="email" value="user@example.com" '
            b'placeholder="Your company email address" id="id_email"></p>',
            response.content)

        self.assertIn(b'<input type="submit" name="submit_input" value="Submit Input">', response.content)
        self.assertIn(b'<button type="submit" name="button_element" value="Button Element">', response.content)
        self.assertIn(b'Button With <strong>Styled</strong> Text', response.content)
        self.assertIn(b'</button>', response.content)

    def test_method_in_view(self):
        """Test that the method is included in the HTML output"""
        c = Client()
        response = c.get('/form-example/')
        self.assertIn(b'<h4>Method: GET</h4>', response.content)

        response = c.post('/form-example/')
        self.assertIn(b'<h4>Method: POST</h4>', response.content)

    @mock.patch('form_example.views.print')
    @mock.patch('form_example.views.OrderForm')
    def test_get_debug_output(self, mock_example_form, mock_print):
        """Mock the print() function to test the debug output with GET request (no output)."""
        mock_request = mock.MagicMock(spec=HttpRequest)
        mock_request.method = 'GET'
        mock_request.POST = QueryDict()
        mock_request.META = {}
        form_example(mock_request)
        mock_example_form.assert_called_with(initial={"email": "user@example.com"})
        mock_print.assert_not_called()

    @mock.patch('form_example.views.print')
    def test_post_debug_output(self, mock_print):
        """Mock the print() function to test the debug output with posted data."""
        mock_request = mock.MagicMock(spec=HttpRequest)
        mock_request.method = 'POST'
        mock_request.POST = QueryDict(
            b'csrfmiddlewaretoken=B0Bda7HRlbhqnREQYbonOzMKgAGFjn3gBT7HXIyq5FSnBFK5iWOz73ucgl3jKtUv&magazine_count=30&'
            b'book_count=20&send_confirmation=on&email=MyEMail%40example.com&submit_input=Submit+Input'
        )
        mock_request.META = {}
        form_example(mock_request)
        mock_print.assert_any_call("magazine_count: (<class 'int'>) 30")
        mock_print.assert_any_call("book_count: (<class 'int'>) 20")
        mock_print.assert_any_call("send_confirmation: (<class 'bool'>) True")
        mock_print.assert_any_call("email: (<class 'str'>) myemail@example.com")

    def test_order_form_valid_all_fields(self):
        """Test the OrderForm with valid data."""
        form = OrderForm({
            "magazine_count": "20",
            "book_count": "50",
            "send_confirmation": "on",
            "email": "User.Name@example.com"
        })

        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data["magazine_count"], 20)
        self.assertEqual(form.cleaned_data["book_count"], 50)
        self.assertTrue(form.cleaned_data["send_confirmation"])

        # this also is a test of email cleaning (to lowercase)
        self.assertEqual(form.cleaned_data["email"], "user.name@example.com")

    def test_order_form_valid_quantity_only(self):
        """Test the OrderForm is valid with only quantities supplied."""
        form = OrderForm({
            "magazine_count": "20",
            "book_count": "50"
        })

        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data["magazine_count"], 20)
        self.assertEqual(form.cleaned_data["book_count"], 50)
        self.assertFalse(form.cleaned_data["send_confirmation"])
        self.assertEqual(form.cleaned_data["email"], "")

    def test_order_form_quantity_exceeded(self):
        """Test the OrderForm has a non-field error when the totals exceed 100."""
        form = OrderForm({
            "magazine_count": "80",
            "book_count": "50",
            "send_confirmation": "on",
            "email": "User.Name@example.com"
        })

        self.assertFalse(form.is_valid())

        self.assertEqual(form.non_field_errors(), ["The total number of items must be 100 or less."])

    def test_email_required_on_send_confirmation(self):
        """
        The email should only be required if send_confirmation is on. Likewise send_confirmation must be on if email
        address is entered.
        """
        form = OrderForm({
            "magazine_count": "80",
            "book_count": "50",
            "email": "User.Name@example.com"
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["send_confirmation"],
                         ["Please check this if you want to receive a confirmation email."])

        form = OrderForm({
            "magazine_count": "80",
            "book_count": "50",
            "send_confirmation": "on"
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["Please enter an email address to receive the confirmation message."])

    def test_email_domain_validation(self):
        """Test that only emails on the example.com domain are accepted."""
        form = OrderForm({
            "magazine_count": "80",
            "book_count": "50",
            "email": "User.Name@notexample.com"
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["email"], ["The email address must be on the domain example.com."])
