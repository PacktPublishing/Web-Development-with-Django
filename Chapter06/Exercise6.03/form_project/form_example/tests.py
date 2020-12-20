import re
from unittest import mock

from django import forms
from django.http import HttpRequest, QueryDict
from django.test import Client
from django.test import TestCase

from form_example.forms import ExampleForm, RADIO_CHOICES, BOOK_CHOICES
from form_example.views import form_example


class Exercise3Test(TestCase):
    def test_fields_in_view(self):
        """"
        Test that some fields exist in the rendered template, assume that if all the fields exist on the form class
        (there is a separate test for this) then they will all be rendered. There's no reason why only some would be.
        """
        c = Client()
        response = c.get('/form-example/')

        self.assertIsNotNone(re.search(r'<input type="hidden" name="csrfmiddlewaretoken" value="\w+">',
                                       response.content.decode('ascii')))

        self.assertIn(b'<p><label for="id_text_input">Text input:</label> <input type="text" name="text_input" '
                      b'required id="id_text_input"></p>', response.content)
        self.assertIn(b'<label for="id_password_input">Password input:</label> <input type="password" '
                      b'name="password_input" required id="id_password_input"></p>', response.content)
        self.assertIn(b'<p><label for="id_checkbox_on">Checkbox on:</label> <input type="checkbox" '
                      b'name="checkbox_on" required id="id_checkbox_on"></p>', response.content)

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
    def test_get_debug_output(self, mock_print):
        """Mock the print() function to test the debug output with GET request (no output)."""
        mock_request = mock.MagicMock(spec=HttpRequest)
        mock_request.method = 'GET'
        mock_request.POST = QueryDict()
        mock_request.META = {}
        form_example(mock_request)
        mock_print.assert_not_called()

    @mock.patch('form_example.views.print')
    def test_post_debug_output(self, mock_print):
        """Mock the print() function to test the debug output with posted data."""
        mock_request = mock.MagicMock(spec=HttpRequest)
        mock_request.method = 'POST'
        mock_request.POST = QueryDict(
            b'csrfmiddlewaretoken=I6vbozNPwTAccdT5dbxgWL4gRAX4DSkTIZ1FbaEognb9q1ZkxWXsffMIRlkI4Yb8&text_input=Some+text'
            b'&password_input=password&checkbox_on=on&radio_input=Value+Two&favorite_book=1&books_you_own=1'
            b'&books_you_own=4&text_area=This+is+my+text.&integer_input=10&float_input=10.5&decimal_input=11.5'
            b'&email_input=user%40example.com&date_input=2019-12-19&hidden_input=Hidden+Value&submit_input=Submit+Input'
        )
        mock_request.META = {}
        form_example(mock_request)
        mock_print.assert_any_call(
            "csrfmiddlewaretoken: ['I6vbozNPwTAccdT5dbxgWL4gRAX4DSkTIZ1FbaEognb9q1ZkxWXsffMIRlkI4Yb8']")
        mock_print.assert_any_call("text_input: ['Some text']")
        mock_print.assert_any_call("password_input: ['password']")
        mock_print.assert_any_call("checkbox_on: ['on']")
        mock_print.assert_any_call("radio_input: ['Value Two']")
        mock_print.assert_any_call("favorite_book: ['1']")
        mock_print.assert_any_call("books_you_own: ['1', '4']")
        mock_print.assert_any_call("text_area: ['This is my text.']")
        mock_print.assert_any_call("integer_input: ['10']")
        mock_print.assert_any_call("float_input: ['10.5']")
        mock_print.assert_any_call("decimal_input: ['11.5']")
        mock_print.assert_any_call("email_input: ['user@example.com']")
        mock_print.assert_any_call("date_input: ['2019-12-19']")
        mock_print.assert_any_call("hidden_input: ['Hidden Value']")
        mock_print.assert_any_call("submit_input: ['Submit Input']")

    def test_example_form(self):
        """Test that the ExampleForm class exists and has the attributes we expect."""
        form = ExampleForm()
        self.assertIsInstance(form.fields['text_input'], forms.CharField)

        self.assertIsInstance(form.fields['password_input'], forms.CharField)
        self.assertIsInstance(form.fields['password_input'].widget, forms.PasswordInput)

        self.assertIsInstance(form.fields['checkbox_on'], forms.BooleanField)

        self.assertIsInstance(form.fields['radio_input'], forms.ChoiceField)
        self.assertIsInstance(form.fields['radio_input'].widget, forms.RadioSelect)
        self.assertEqual(form.fields['radio_input'].choices, list(RADIO_CHOICES))

        self.assertIsInstance(form.fields['favorite_book'], forms.ChoiceField)
        self.assertEqual(form.fields['favorite_book'].choices, list(BOOK_CHOICES))

        self.assertIsInstance(form.fields['books_you_own'], forms.MultipleChoiceField)
        self.assertEqual(form.fields['books_you_own'].choices, list(BOOK_CHOICES))

        self.assertIsInstance(form.fields['text_area'], forms.CharField)
        self.assertIsInstance(form.fields['text_area'].widget, forms.Textarea)

        self.assertIsInstance(form.fields['integer_input'], forms.IntegerField)

        self.assertIsInstance(form.fields['float_input'], forms.FloatField)

        self.assertIsInstance(form.fields['decimal_input'], forms.DecimalField)

        self.assertIsInstance(form.fields['email_input'], forms.EmailField)

        self.assertIsInstance(form.fields['date_input'], forms.DateField)
        self.assertIsInstance(form.fields['date_input'].widget, forms.DateInput)
        self.assertEqual(form.fields['date_input'].widget.input_type, 'date')

        self.assertIsInstance(form.fields['hidden_input'], forms.CharField)
        self.assertEqual(form.fields['hidden_input'].initial, 'Hidden Value')
