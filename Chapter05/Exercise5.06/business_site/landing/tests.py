from django.conf import settings
from django.test import TestCase


class Exercise6Test(TestCase):
    """
    This has only one test. We assume if we got to this point and the other exercises were OK we don't need to test
    Django's ManifestFileStorage. Just that it has been set properly.
    """

    def test_django_conf(self):
        """
        Check that `landing` is in `settings.INSTALLED_APPS`, the static dir is set to <projectdir>/static, and
        STATIC_ROOT is set to the static_production_test directory, amd that STATICFILES_STORAGE is set to
        'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
        """
        self.assertIn('landing', settings.INSTALLED_APPS)
        self.assertEquals([settings.BASE_DIR + '/static'], settings.STATICFILES_DIRS)
        self.assertEquals(settings.BASE_DIR + '/static_production_test', settings.STATIC_ROOT)
        self.assertEquals(
            settings.STATICFILES_STORAGE, 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage')
