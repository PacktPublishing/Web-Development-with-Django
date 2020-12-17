import os

from django.test import TestCase
from django.conf import settings


class Exercise5TestCase(TestCase):
    def test_template_content(self):
        """Test that base.html exists and has the expected content"""
        template_path = os.path.join(settings.BASE_DIR, 'reviews/templates/base.html')
        self.assertTrue(os.path.exists(template_path))
        with open(template_path) as tf:
            contents = tf.read()

        self.assertIn('Hello from a template!', contents)
