import os

from django.conf import settings
from django.test import TestCase, Client


class Exercise4Test(TestCase):
    def test_crispy_settings(self):
        """Test that the right settings are configured for Django Crispy Forms."""
        self.assertIn('crispy_forms', settings.INSTALLED_APPS)
        self.assertEquals(settings.CRISPY_TEMPLATE_PACK, 'bootstrap4')

    def test_crispy_form_used_in_template(self):
        """Test that the {% crispy %} template tag is being used to render the form in search-results.html"""
        with open(os.path.join(settings.BASE_DIR, 'reviews/templates/reviews/search-results.html')) as tf:
            template_content = tf.read()
            self.assertIn('{% load crispy_forms_tags %', template_content)
            self.assertIn('{% crispy form %}', template_content)
            self.assertNotIn('<form', template_content)
            self.assertNotIn('</form>', template_content)

    def test_rendered_form(self):
        """Test the rendered form view."""
        c = Client()
        resp = c.get('/book-search/')
        self.assertIn(b'<form', resp.content)
        self.assertIn(
            b'<input type="text" name="search" minlength="3" class="textinput textInput form-control" id="id_search">',
            resp.content)
        self.assertIn(b'<select name="search_in" class="select form-control" id="id_search_in">', resp.content)
