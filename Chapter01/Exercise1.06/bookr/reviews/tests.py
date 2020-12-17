from django.test import TestCase
from django.test import Client


class Exercise6TestCase(TestCase):
    def test_template_render(self):
        """Test that the index view now returns the rendered template."""
        c = Client()

        response = c.get('/')
        self.assertIn(b'Hello from a template!', response.content)
