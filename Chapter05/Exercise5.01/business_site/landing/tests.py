import os
from urllib.request import urlopen

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class Exercise1Test(StaticLiveServerTestCase):
    """
    These tests use `StaticLiveServerTestCase` and `urlopen` since the normal `TestCase` uses a special server that does
    not serve static assets.
    """

    def test_django_conf(self):
        """Check that `landing` is in `settings.INSTALLED_APPS` and that the static dir is not manually defined."""
        self.assertIn('landing', settings.INSTALLED_APPS)
        self.assertEquals(0, len(settings.STATICFILES_DIRS))

    def test_logo_get(self):
        """
        Test that the logo.png can be downloaded, and the content matches that on disk. This also checks the logo.png is
        in the right location and is being served using the static files finder.
        """
        response = urlopen(self.live_server_url + '/static/landing/logo.png').read()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, 'static', 'landing', 'logo.png'), 'rb') as f:
            self.assertEqual(response, f.read())
