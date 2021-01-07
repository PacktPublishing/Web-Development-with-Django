from configurations import values
from django.test import TestCase

from bookr import settings as direct_settings


class Exercise2Test(TestCase):
    def test_dj_database_url(self):
        """Test that the DATABASES is being set with a URL."""
        # since we are running in DEBUG mode we can check how the values were set on the non-active conf
        self.assertFalse(direct_settings.Prod.DEBUG)
        self.assertIsInstance(direct_settings.Prod.DATABASES, values.DatabaseURLValue)
        self.assertEquals(direct_settings.Prod.DATABASES.environ_prefix, 'DJANGO')
