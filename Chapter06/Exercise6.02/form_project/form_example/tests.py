import re

from django.http import HttpRequest, QueryDict
from django.test import TestCase
from django.test import Client

from unittest import mock

from form_example.views import form_example


class Exercise2Test(TestCase):
    def test_fields_in_view(self):
        """"Test that all the fields we defined appear in the HTML from the view, including newly-added CSRF token."""
        c = Client()
        response = c.get('/form-example/')

        self.assertIsNotNone(re.search(r'<input type="hidden" name="csrfmiddlewaretoken" value="\w+">',
                                       response.content.decode('ascii')))

        self.assertIn(b'<label for="id_text_input">Text Input</label><br>', response.content)
        self.assertIn(
            b'<input id="id_text_input" type="text" name="text_input" value="" placeholder="Enter some text">',
            response.content)

        self.assertIn(b'<label for="id_password_input">Password Input</label><br>', response.content)
        self.assertIn(
            b'<input id="id_password_input" type="password" name="password_input" value="" '
            b'placeholder="Your password">', response.content)

        self.assertIn(
            b'<input id="id_checkbox_input" type="checkbox" name="checkbox_on" value="Checkbox Checked" checked>',
            response.content)
        self.assertIn(b'<label for="id_checkbox_input">Checkbox</label>', response.content)

        self.assertIn(b'<input id="id_radio_one_input" type="radio" name="radio_input" value="Value One">',
                      response.content)
        self.assertIn(b'<label for="id_radio_one_input">Value One</label>', response.content)
        self.assertIn(b'<input id="id_radio_two_input" type="radio" name="radio_input" value="Value Two" checked>',
                      response.content)
        self.assertIn(b'<label for="id_radio_two_input">Value Two</label>', response.content)
        self.assertIn(b'<input id="id_radio_three_input" type="radio" name="radio_input" value="Value Three">',
                      response.content)
        self.assertIn(b'<label for="id_radio_three_input">Value Three</label>', response.content)

        self.assertIn(b'<label for="id_favorite_book">Favorite Book</label><br>', response.content)
        self.assertIn(b'<select id="id_favorite_book" name="favorite_book">', response.content)
        self.assertIn(b'<optgroup label="Non-Fiction">', response.content)
        self.assertIn(b'<option value="1">Deep Learning with Keras</option>', response.content)
        self.assertIn(b'<option value="2">Web Development with Django</option>', response.content)
        self.assertIn(b'<optgroup label="Fiction">', response.content)
        self.assertIn(b'<option value="3">Brave New World</option>', response.content)
        self.assertIn(b'<option value="4">The Great Gatsby</option>', response.content)

        self.assertIn(b'<label for="id_books_you_own">Books You Own</label><br>', response.content)
        self.assertIn(b'<select id="id_books_you_own" name="books_you_own" multiple>', response.content)
        self.assertIn(b'<optgroup label="Non-Fiction">', response.content)
        self.assertIn(b'<option value="1">Deep Learning with Keras</option>', response.content)
        self.assertIn(b'<option value="2">Web Development with Django</option>', response.content)
        self.assertIn(b'<optgroup label="Fiction">', response.content)
        self.assertIn(b'<option value="3">Brave New World</option>', response.content)
        self.assertIn(b'<option value="4">The Great Gatsby</option>', response.content)

        self.assertIn(b'<label for="id_text_area">Text Area</label><br>', response.content)
        self.assertIn(
            b'<textarea name="text_area" id="id_text_area" placeholder="Enter multiple lines of text"></textarea>',
            response.content)
        self.assertIn(b'<label for="id_number_input">Number Input</label><br>', response.content)
        self.assertIn(
            b'<input id="id_number_input" type="number" name="number_input" value="" step="any" '
            b'placeholder="A number">', response.content)
        self.assertIn(b'<label for="id_email_input">Email Input</label><br>', response.content)
        self.assertIn(
            b'<input id="id_email_input" type="email" name="email_input" value="" placeholder="Your email address">',
            response.content)
        self.assertIn(b'<label for="id_date_input">Date Input</label><br>', response.content)
        self.assertIn(b'<input id="id_date_input" type="date" name="date_input" value="2019-11-23">', response.content)
        self.assertIn(b'<input type="submit" name="submit_input" value="Submit Input">', response.content)
        self.assertIn(b'<button type="submit" name="button_element" value="Button Element">', response.content)
        self.assertIn(b'Button With <strong>Styled</strong> Text', response.content)
        self.assertIn(b'</button>', response.content)
        self.assertIn(b'<input type="hidden" name="hidden_input" value="Hidden Value">', response.content)

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
        mock_request.POST = QueryDict(b'csrfmiddlewaretoken='
                                      b'QgK9FsIIlrh5VJrq35Y9LnlLWLxn59XzQ9gDs3zh5VS29xxFnQol4R3dWwU1wfOO&'
                                      b'text_input=Text&password_input=Password&checkbox_on=Checkbox+Checked&'
                                      b'radio_input=Value+Two&favorite_book=1&books_you_own=1&books_you_own=3&'
                                      b'text_area=Text+box+text.&number_input=4.5&email_input=user%40example.com&'
                                      b'date_input=2019-11-23&button_element=Button+Element&hidden_input=Hidden+Value')
        mock_request.META = {}
        form_example(mock_request)
        mock_print.assert_any_call(
            "csrfmiddlewaretoken: ['QgK9FsIIlrh5VJrq35Y9LnlLWLxn59XzQ9gDs3zh5VS29xxFnQol4R3dWwU1wfOO']")
        mock_print.assert_any_call("text_input: ['Text']")
        mock_print.assert_any_call("password_input: ['Password']")
        mock_print.assert_any_call("checkbox_on: ['Checkbox Checked']")
        mock_print.assert_any_call("radio_input: ['Value Two']")
        mock_print.assert_any_call("favorite_book: ['1']")
        mock_print.assert_any_call("books_you_own: ['1', '3']")
        mock_print.assert_any_call("text_area: ['Text box text.']")
        mock_print.assert_any_call("number_input: ['4.5']")
        mock_print.assert_any_call("email_input: ['user@example.com']")
        mock_print.assert_any_call("date_input: ['2019-11-23']")
        mock_print.assert_any_call("button_element: ['Button Element']")
        mock_print.assert_any_call("hidden_input: ['Hidden Value']")
