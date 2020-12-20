import os
from urllib.request import urlopen

from django.conf import settings
from django.test import LiveServerTestCase


class Exercise1Test(LiveServerTestCase):
    def test_media_serving(self):
        """Test that our test.txt file can be retrieved using the media URL."""
        media_root = settings.MEDIA_ROOT
        self.assertEqual(settings.MEDIA_URL, '/media/')

        with open(os.path.join(media_root, 'test.txt'), 'rb') as f:
            hw_content = f.read()

        resp = urlopen(self.live_server_url + '/media/test.txt')

        self.assertEquals(hw_content, resp.read())
