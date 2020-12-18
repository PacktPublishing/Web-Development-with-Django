from django.test import TestCase
from django.test import Client


class Activity2Test(TestCase):
    def test_index_page(self):
        """Test the Bookr welcome screen"""
        c = Client()
        response = c.get('/')
        self.assertIn(b'<title>Welcome to Bookr</title>', response.content)
        self.assertIn(b'<h1>Welcome to Bookr</h1>', response.content)

    def test_no_search(self):
        """Test output when no query string is set."""
        c = Client()
        response = c.get('/book-search')
        self.assertIn(b'<title>Search Results: </title>', response.content)
        self.assertIn(b'<h1>Search Results for <em></em></h1>', response.content)

    def test_empty_search(self):
        """Result for empty string search should be the same as previous test."""
        c = Client()
        response = c.get('/book-search?search=')
        self.assertIn(b'<title>Search Results: </title>', response.content)
        self.assertIn(b'<h1>Search Results for <em></em></h1>', response.content)

    def test_basic_search(self):
        """Basic search should just pass through the value."""
        c = Client()
        response = c.get('/book-search?search=Test Search')
        self.assertIn(b'<title>Search Results: Test Search</title>', response.content)
        self.assertIn(b'<h1>Search Results for <em>Test Search</em></h1>', response.content)

    def test_html_search(self):
        """Test that HTML entities are escaped in the output when searching for them."""
        c = Client()
        response = c.get('/book-search?search=</html>')
        self.assertIn(b'<title>Search Results: &lt;/html&gt;</title>', response.content)
        self.assertIn(b'<h1>Search Results for <em>&lt;/html&gt;</em></h1>', response.content)
