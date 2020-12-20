import os
from urllib.request import urlopen

from django.conf import settings
from django.test import LiveServerTestCase, Client


class Exercise2Test(LiveServerTestCase):
    def test_media_serving(self):
        """Test that our test.txt file can be retrieved using the media URL."""
        media_root = settings.MEDIA_ROOT
        self.assertEqual(settings.MEDIA_URL, '/media/')

        with open(os.path.join(media_root, 'test.txt'), 'rb') as f:
            hw_content = f.read()

        resp = urlopen(self.live_server_url + '/media/test.txt')

        self.assertEquals(hw_content, resp.read())

    def test_media_example_view(self):
        """
        Test the media example view is set up correctly and contains a link to the test.txt file in the template it
        renders.
        """
        c = Client()
        resp = c.get('/media-example/')
        self.assertIn(b'<a href="/media/test.txt">Test Text File</a>', resp.content)
