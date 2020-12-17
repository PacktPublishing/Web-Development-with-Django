from django.test import TestCase
from django.test import Client


class Exercise7TestCase(TestCase):
    def test_template_render(self):
        """Test that the index view now returns the rendered template."""
        c = Client()

        response = c.get('/')
        self.assertIn(b'<title>Title</title>', response.content)  # check that it is HTML
        self.assertIn(b'Hello, world!', response.content)
