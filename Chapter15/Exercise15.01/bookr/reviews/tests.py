from configurations import Configuration, values
from django.test import TestCase

from bookr import settings as direct_settings


class Exercise1Test(TestCase):
    def test_configurations_refactoring(self):
        """Import the settings file directly to check that the Dev/Prod classes have been configured."""
        self.assertTrue(issubclass(direct_settings.Dev, Configuration))
        self.assertTrue(issubclass(direct_settings.Prod, direct_settings.Dev))

        # since we are running in DEBUG mode we can't check how these values were set
        self.assertTrue(direct_settings.Dev.DEBUG)
        self.assertEqual(direct_settings.Dev.ALLOWED_HOSTS, [])
        self.assertIsInstance(direct_settings.Dev.SECRET_KEY, str)

        # since we are running in DEBUG mode we can check how the values were set on the non-active conf
        self.assertFalse(direct_settings.Prod.DEBUG)
        self.assertIsInstance(direct_settings.Prod.ALLOWED_HOSTS, values.ListValue)
        self.assertIsInstance(direct_settings.Prod.SECRET_KEY, values.SecretValue)
