import os
from io import BytesIO
from urllib.request import urlopen

from django.conf import settings
from django.test import LiveServerTestCase, Client


class Exercise3Test(LiveServerTestCase):
    def test_media_example_upload(self):
        """
        Test the upload functionality to the media_example view. Check it can be downloaded again.
        """
        test_data = b'some test data'
        filename = 'exercise_3_test.txt'
        save_path = os.path.join(settings.MEDIA_ROOT, filename)
        fp = BytesIO(test_data)
        fp.name = filename

        try:
            c = Client()
            resp = c.post('/media-example/', {'file_upload': fp})
            self.assertEquals(resp.status_code, 200)

            with open(save_path, 'rb') as uploaded_fp:
                self.assertEquals(uploaded_fp.read(), test_data)

            media_file = urlopen(self.live_server_url + '/media/' + filename)

            self.assertEquals(media_file.read(), test_data)
        finally:
            if os.path.exists(save_path):
                os.unlink(save_path)
