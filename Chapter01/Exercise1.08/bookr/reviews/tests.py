from django.test import TestCase
from django.test import Client


class Exercise8TestCase(TestCase):
    def test_exception(self):
        """The view should raise a NameError exception"""
        c = Client()
        with self.assertRaises(NameError):
            c.get('/')
