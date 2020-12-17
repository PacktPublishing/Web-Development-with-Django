from django.test import TestCase
from django.test import Client


class Exercise4TestCase(TestCase):
    def test_template_content(self):
        """Test that the index view returns the set names from the paramaters, or defaults to 'world'"""
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello, world!')

        response = c.get('/?name=Ben')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello, Ben!')

        response = c.get('/?name=Ben&name=John')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello, John!')

        response = c.get('/?name=')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello, world!')
