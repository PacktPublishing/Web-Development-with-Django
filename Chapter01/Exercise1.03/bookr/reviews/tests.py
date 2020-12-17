from django.test import TestCase
from django.test import Client


class Exercise3TestCase(TestCase):
    def test_index_view(self):
        """Test that the index view returns Hello, world!"""
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello, world!')
