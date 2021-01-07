import os
from unittest import mock

from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase

from reviews.forms import InstanceForm, PublisherForm, ReviewForm, BookMediaForm
from reviews.models import Book
from reviews.views import book_media


class Activity1Test(TestCase):
    def test_crispy_form_used_in_template(self):
        """Test that the {% crispy %} template tag is being used to render the form in search-results.html"""
        with open(os.path.join(settings.BASE_DIR, 'reviews/templates/reviews/instance-form.html')) as tf:
            template_content = tf.read()
            self.assertIn('{% load crispy_forms_tags %', template_content)
            self.assertIn('{% crispy form %}', template_content)
            self.assertNotIn('<form', template_content)
            self.assertNotIn('</form>', template_content)

    def test_form_helper(self):
        """
        Test that InstanceForm has a helper with a submit button, the button text changes based on the existence of the
        instance argument. We can't test this on InstanceForm directly since it can't be instantiated without a model.
        Instead run the same test on each form that inherits from it, then check their inheritance.
        """
        for form_class in (PublisherForm, ReviewForm, BookMediaForm):
            form = form_class()
            self.assertEquals(form.helper.form_method, 'post')
            self.assertEquals(form.helper.inputs[0].value, 'Create')

            form_with_instance = form_class(instance=form_class.Meta.model())
            self.assertEquals(form_with_instance.helper.form_method, 'post')
            self.assertEquals(form_with_instance.helper.inputs[0].value, 'Save')

            self.assertTrue(issubclass(form_class, InstanceForm))

    @mock.patch('reviews.views.render')
    @mock.patch('reviews.views.BookMediaForm')
    def test_book_media_render_call(self, mock_book_media_form, mock_render):
        """Test that the `render` call in book_media no longer contains `is_file_upload` item."""
        req = mock.MagicMock(spec=HttpRequest, name='request')
        req.user = mock.MagicMock()
        req.user.is_authenticated = True
        req.method = 'GET'
        mock_book = mock.MagicMock(spec=Book, name='book')
        with mock.patch('reviews.views.get_object_or_404', return_value=mock_book) as mock_get_object_or_404:
            resp = book_media(req, 3)
        mock_render.assert_called_with(req, 'reviews/instance-form.html',
                                       {'instance': mock_book, 'form': mock_book_media_form.return_value,
                                        'model_type': 'Book'})
