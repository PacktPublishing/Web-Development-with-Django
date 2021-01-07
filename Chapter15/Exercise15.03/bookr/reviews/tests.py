import os

from django.conf import settings
from django.test import TestCase


class Exercise3Test(TestCase):
    def test_djdt_setup(self):
        """Test that the configuration for Django Debug Toolbar is correct."""
        self.assertIn('debug_toolbar.middleware.DebugToolbarMiddleware', settings.MIDDLEWARE)
        self.assertIn('debug_toolbar', settings.INSTALLED_APPS)
        self.assertEquals(['127.0.0.1'], settings.INTERNAL_IPS)

    def test_djdt_urls(self):
        """
        Test that the DJDT Urls are set up. This is a manual process since DjDT won't render for the test Client,
        and tests run with DEBUG=True so the urlpatterns won't contain the path. This might be a bit fragile.
        """

        with open(os.path.join(settings.BASE_DIR, 'bookr/urls.py')) as sf:
            self.assertIn("       path('__debug__/', include(debug_toolbar.urls))", sf.read())
