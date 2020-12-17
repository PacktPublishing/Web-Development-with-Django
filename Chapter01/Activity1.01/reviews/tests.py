from django.test import TestCase
from django.test import Client


class Activity1Test(TestCase):
    def test_index_page(self):
        """Test the Bookr welcome screen"""
        c = Client()
        response = c.get('/')
        self.assertIn(b'<title>Welcome to Bookr</title>', response.content)
        self.assertIn(b'<h1>Welcome to Bookr</h1>', response.content)

