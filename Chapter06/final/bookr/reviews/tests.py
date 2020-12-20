import os
import re
from unittest import mock

from django import forms
from django.conf import settings
from django.core import management
from django.http import HttpRequest
from django.test import TestCase, Client

from reviews.forms import SearchForm
from reviews.views import book_search


class Activity1Test(TestCase):
    @staticmethod
    def load_csv():
        """Run the loadcsv management command. This is only necessary on some tests."""
        management.call_command('loadcsv', csv=os.path.join(settings.BASE_DIR, 'reviews', 'management', 'commands',
                                                            'WebDevWithDjangoData.csv'))

    def test_search_form_fields(self):
        """Test that the SearchForm is defined with the correct fields."""
        sf = SearchForm()
        self.assertEquals(len(sf.fields), 2)
        self.assertIsInstance(sf.fields['search'], forms.CharField)
        self.assertIsInstance(sf.fields['search_in'], forms.ChoiceField)
        self.assertEquals(sf.fields['search_in'].choices[0][0], 'title')
        self.assertEquals(sf.fields['search_in'].choices[0][1], 'Title')

        self.assertEquals(sf.fields['search_in'].choices[1][0], 'contributor')
        self.assertEquals(sf.fields['search_in'].choices[1][1], 'Contributor')

    def test_form_validity(self):
        """
        Test that SearchForm is valid when we expect: if search is empty or has more than 2 characters. It should also
        be valid if search_in is empty, but not if it has a bad value.
        """

        # These fixtures are a mini suite of tuples, in the form (valid, data dict)
        fixtures = (
            (True, {}),
            (False, {'search': 'ab'}),
            (True, {'search': 'abc'}),
            (True, {'search': 'abc', 'search_in': 'title'}),
            (True, {'search': 'abc', 'search_in': 'contributor'}),
            (False, {'search': 'abc', 'search_in': 'bad'}),
        )

        for expected, form_data in fixtures:
            sf = SearchForm(form_data)
            self.assertEquals(sf.is_valid(), expected)

    @mock.patch('reviews.views.render')
    @mock.patch('reviews.views.SearchForm')
    def test_book_search_without_input(self, mock_search_form_init, mock_render):
        """The book search view should render with an empty set if no input is provided."""
        mock_request = mock.MagicMock(name='request', spec=HttpRequest)
        mock_search_form_init.return_value.is_valid.return_value = False
        mock_request.GET = {}

        resp = book_search(mock_request)

        self.assertEquals(resp, mock_render.return_value)

        mock_search_form_init.assert_called_with(mock_request.GET)
        mock_render.assert_called_with(mock_request, 'reviews/search-results.html',
                                       {'form': mock_search_form_init.return_value, 'search_text': '', 'books': set()})

    @mock.patch('reviews.views.render')
    @mock.patch('reviews.views.SearchForm')
    def test_book_search_title(self, mock_search_form_init, mock_render):
        """The book search view should render with title search results when searching and no search_in is provided."""
        self.load_csv()

        mock_request = mock.MagicMock(name='request', spec=HttpRequest)

        mock_request.GET = {'search': 'keras'}

        # this makes it easier to use assert_calls_with since we know what the 'form' item is
        mock_search_form_init.return_value = SearchForm(mock_request.GET)

        resp = book_search(mock_request)

        self.assertEquals(resp, mock_render.return_value)

        mock_search_form_init.assert_called_with(mock_request.GET)
        self.assertEquals(mock_render.call_count, 1)

        self.assertEquals(mock_render.call_args[0][0], mock_request)
        self.assertEquals(mock_render.call_args[0][1], 'reviews/search-results.html')
        self.assertEquals(mock_render.call_args[0][2]['form'], mock_search_form_init.return_value)
        self.assertEquals(mock_render.call_args[0][2]['search_text'], 'keras')

        self.assertEquals(len(mock_render.call_args[0][2]['books']), 1)
        for book in mock_render.call_args[0][2]['books']:
            self.assertEquals(book.title, 'Advanced Deep Learning with Keras')

    @mock.patch('reviews.views.render')
    @mock.patch('reviews.views.SearchForm')
    def test_book_search_contributor(self, mock_search_form_init, mock_render):
        """The book search view should render with contributor name search results when search_in is contributor."""
        self.load_csv()

        mock_request = mock.MagicMock(name='request', spec=HttpRequest)

        mock_request.GET = {'search': 'king', 'search_in': 'contributor'}

        # this makes it easier to use assert_calls_with since we know what the 'form' item is
        mock_search_form_init.return_value = SearchForm(mock_request.GET)

        resp = book_search(mock_request)

        self.assertEquals(resp, mock_render.return_value)

        mock_search_form_init.assert_called_with(mock_request.GET)
        self.assertEquals(mock_render.call_count, 1)

        self.assertEquals(mock_render.call_args[0][0], mock_request)
        self.assertEquals(mock_render.call_args[0][1], 'reviews/search-results.html')
        self.assertEquals(mock_render.call_args[0][2]['form'], mock_search_form_init.return_value)
        self.assertEquals(mock_render.call_args[0][2]['search_text'], 'king')

        self.assertEquals(len(mock_render.call_args[0][2]['books']), 1)
        for book in mock_render.call_args[0][2]['books']:
            self.assertEquals(book.title, 'The Talisman')

    def test_base_template(self):
        """Test that the base.html template has had the right form attributes added."""
        with open(os.path.join(settings.BASE_DIR, 'templates', 'base.html')) as base_tp:
            content = base_tp.read()

        self.assertIn('<form action="{% url \'book_search\' %}"', content)
        self.assertIn('name="search" value="{{ search_text }}" minlength="3">', content)
        self.assertIn('<title>{% block title %}Bookr{% endblock %}</title>', content)

    def test_page_no_search(self):
        """Test the parts of the page when no search is specified."""
        self.load_csv()
        c = Client()
        resp = c.get('/book-search/')

        self.assertIn('<title>Book Search</title>', re.sub('\n\s*', '', resp.content.decode('utf8')))
        self.assertNotIn(b'<h3>Search Results for', resp.content)
        self.assertNotIn(b'<span class="text-info">Title: </span>', resp.content)

    def test_page_with_search(self):
        """Test the parts of the page when a search is specified."""
        self.load_csv()
        c = Client()
        resp = c.get('/book-search/?search=keras')

        self.assertIn('<title>Search Results for "keras"</title>', re.sub('\n\s*', '', resp.content.decode('utf8')))
        self.assertIn(b'<h3>Search Results for <em>keras</em></h3>', resp.content)
        self.assertIn(b'<a href="/books/1/">Advanced Deep Learning with Keras (9781788629416)</a>', resp.content)
        self.assertIn(b'<span class="text-info">Contributors: </span>', resp.content)
        self.assertIn(b'Rowel Atienza', resp.content)

    def test_page_with_search_no_results(self):
        """Test the parts of the page when a search is specified."""
        self.load_csv()
        c = Client()
        resp = c.get('/book-search/?search=abc123')

        self.assertIn('<title>Search Results for "abc123"</title>', re.sub('\n\s*', '', resp.content.decode('utf8')))
        self.assertIn(b'<h3>Search Results for <em>abc123</em></h3>', resp.content)
        self.assertIn(b'<li class="list-group-item">No results found.</li>', resp.content)
        self.assertNotIn(b'<span class="text-info">Title: </span>', resp.content)
