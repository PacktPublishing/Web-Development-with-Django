import os
from shutil import rmtree

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase


def read_content(path):
    with open(path) as f:
        return f.read()


class Exercise4Test(TestCase):
    def test_django_conf(self):
        """
        Check that `landing` is in `settings.INSTALLED_APPS`, the static dir is set to <projectdir>/static, and
        STATIC_ROOT is set to the static_production_test directory.
        """
        self.assertIn('landing', settings.INSTALLED_APPS)
        self.assertEquals([settings.BASE_DIR + '/static'], settings.STATICFILES_DIRS)
        self.assertEquals(settings.BASE_DIR + '/static_production_test', settings.STATIC_ROOT)

    def test_collect_static(self):
        """Test the result of the collectstatic command."""
        static_output_dir = os.path.join(settings.BASE_DIR, 'static_production_test')
        call_command('collectstatic', '--noinput')
        self.assertTrue(os.path.isdir(static_output_dir))
        self.assertTrue(os.path.isdir(os.path.join(static_output_dir, 'admin')))
        self.assertTrue(os.path.exists(os.path.join(static_output_dir, 'landing', 'logo.png')))
        self.assertTrue(os.path.exists(os.path.join(static_output_dir, 'main.css')))
        rmtree(static_output_dir)
