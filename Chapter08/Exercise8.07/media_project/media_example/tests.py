from unittest import mock

import os
from django import forms
from django.conf import settings
from django.test import LiveServerTestCase, Client
from media_example.forms import UploadForm
from media_example.models import ExampleModel
from media_example.views import media_example
from urllib.request import urlopen


class Exercise7Test(LiveServerTestCase):
    def test_form_definition(self):
        """Test that the UploadForm has the correct field."""
        f = UploadForm()
        self.assertEquals(f.Meta.model, ExampleModel)
        self.assertEquals(f.Meta.fields, '__all__')
        self.assertIsInstance(f.fields['image_field'], forms.ImageField)
        self.assertIsInstance(f.fields['file_field'], forms.FileField)

    def test_form_in_template(self):
        """Test that the form is in the rendered template."""
        c = Client()
        resp = c.get('/media-example/')
        self.assertEquals(resp.status_code, 200)
        self.assertIn(b'<label for="id_file_field">File field:</label>', resp.content)
        self.assertIn(b'<label for="id_image_field">Image field:</label>', resp.content)
        self.assertIn(b'<input type="file" name="image_field" accept="image/*" required id="id_image_field">',
                      resp.content)
        self.assertIn(b'<input type="file" name="file_field" required id="id_file_field">',
                      resp.content)

    @mock.patch('media_example.views.render', name='render')
    def test_render_call(self, mock_render):
        """Test that the view calls render with the correct arguments and returns it."""
        request = mock.MagicMock(name='request')
        resp = media_example(request)

        self.assertEquals(resp, mock_render.return_value)
        self.assertEquals(mock_render.call_args[0][0], request)
        self.assertEquals(mock_render.call_args[0][1], 'media-example.html')
        self.assertIsInstance(mock_render.call_args[0][2], dict)
        self.assertEquals(len(mock_render.call_args[0][2]), 2)
        self.assertIsInstance(mock_render.call_args[0][2]['form'], UploadForm)
        self.assertIsNone(mock_render.call_args[0][2]['instance'], UploadForm)

    def test_media_example_upload(self):
        """
        Test the upload functionality to the media_example view. Check it can be downloaded again.
        """
        logo_filename = 'cover.jpg'
        logo_save_path = os.path.join(settings.MEDIA_ROOT, 'images', logo_filename)

        css_filename = 'sample.txt'
        css_save_path = os.path.join(settings.MEDIA_ROOT, 'files', css_filename)

        try:
            c = Client()
            with open(os.path.join(settings.BASE_DIR, 'fixtures', logo_filename), 'rb') as logo_fp:
                with open(os.path.join(settings.BASE_DIR, 'fixtures', css_filename), 'rb') as css_fp:
                    resp = c.post('/media-example/', {'file_field': css_fp, 'image_field': logo_fp})

            self.assertEquals(resp.status_code, 200)
            self.assertIn(b'<img src="/media/images/cover.jpg">', resp.content)

            with open(logo_save_path, 'rb') as uploaded_logo_fp:
                media_file = urlopen(self.live_server_url + '/media/images/' + logo_filename)
                self.assertEquals(media_file.read(), uploaded_logo_fp.read())

            with open(css_save_path, 'rb') as uploaded_css_fp:
                media_file = urlopen(self.live_server_url + '/media/files/' + css_filename)
                self.assertEquals(media_file.read(), uploaded_css_fp.read())

        finally:
            if os.path.exists(logo_save_path):
                os.unlink(logo_save_path)

            if os.path.exists(css_save_path):
                os.unlink(css_save_path)
