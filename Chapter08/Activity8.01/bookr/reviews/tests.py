import os
from unittest import mock

from PIL import Image
from django import forms
from django.conf import settings
from django.test import TestCase, Client
from django.utils import timezone

from reviews.forms import BookMediaForm
from reviews.models import Book, Publisher
from reviews.views import book_media


class Activity1Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        p = Publisher.objects.create(name='Test Publisher')
        b = Book.objects.create(title='Test Book', publication_date=timezone.now(), publisher=p)

    def test_form_definition(self):
        """Test that the BookMediaForm has the correct field."""
        f = BookMediaForm()
        self.assertEquals(f.Meta.model, Book)
        self.assertEquals(f.Meta.fields, ['cover', 'sample'])
        self.assertIsInstance(f.fields['cover'], forms.ImageField)
        self.assertIsInstance(f.fields['sample'], forms.FileField)

    def test_form_in_template(self):
        """Test that the form is in the rendered template."""
        c = Client()
        resp = c.get('/books/1/media/')
        self.assertEquals(resp.status_code, 200)
        self.assertIn(b'<label for="id_sample">Sample:</label>', resp.content)
        self.assertIn(b'<label for="id_cover">Cover:</label>', resp.content)
        self.assertIn(b'<input type="file" name="cover" accept="image/*" id="id_cover">',
                      resp.content)
        self.assertIn(b'<input type="file" name="sample" id="id_sample">',
                      resp.content)

    @mock.patch('reviews.views.render', name='render')
    @mock.patch('reviews.views.get_object_or_404', name='get_object_or_404')
    def test_render_call(self, mock_g_o_o_404 ,mock_render):
        """Test that the view calls render with the correct arguments and returns it."""
        request = mock.MagicMock(name='request')
        resp = book_media(request, 'pk')

        mock_g_o_o_404.assert_called_with(Book, pk='pk')
        self.assertEquals(resp, mock_render.return_value)
        self.assertEquals(mock_render.call_args[0][0], request)
        self.assertEquals(mock_render.call_args[0][1], 'reviews/instance-form.html')
        self.assertIsInstance(mock_render.call_args[0][2], dict)
        self.assertEquals(len(mock_render.call_args[0][2]), 4)
        self.assertIsInstance(mock_render.call_args[0][2]['form'], BookMediaForm)
        self.assertEquals(mock_render.call_args[0][2]['instance'], mock_g_o_o_404.return_value)
        self.assertEquals(mock_render.call_args[0][2]['model_type'], 'Book')
        self.assertEquals(mock_render.call_args[0][2]['is_file_upload'], True)

    def test_book_media_upload(self):
        """
        Test the upload functionality to the book_media view. Check it exists on disk and the image has been resized.
        """
        cover_filename = 'machine-learning-for-algorithmic-trading.png'
        cover_save_path = os.path.join(settings.MEDIA_ROOT, 'book_covers', cover_filename)

        sample_filename = 'machine-learning-for-trading.pdf'
        sample_save_path = os.path.join(settings.MEDIA_ROOT, 'book_samples', sample_filename)

        try:
            c = Client()
            with open(os.path.join(settings.BASE_DIR, 'fixtures', cover_filename), 'rb') as cover_fp:
                with open(os.path.join(settings.BASE_DIR, 'fixtures', sample_filename), 'rb') as sample_fp:
                    resp = c.post('/books/1/media/', {'cover': cover_fp, 'sample': sample_fp})

            self.assertEquals(resp.status_code, 302)
            self.assertEquals(resp['Location'], '/books/1/')

            with open(cover_save_path, 'rb') as cover_image_fp:
                cover = Image.open(cover_image_fp)
                self.assertTrue(cover.width == 300 or cover.height == 300)

        finally:
            if os.path.exists(cover_save_path):
                os.unlink(cover_save_path)

            if os.path.exists(sample_save_path):
                os.unlink(sample_save_path)
