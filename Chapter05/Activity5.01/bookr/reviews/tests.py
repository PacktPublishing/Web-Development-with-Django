import os
from urllib.request import urlopen

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client


def read_content(path):
    with open(path) as f:
        return f.read()


class Activity1Test(StaticLiveServerTestCase):
    """
    These tests use `StaticLiveServerTestCase` and `urlopen` since the normal `TestCase` uses a special server that does
    not serve static assets.
    """

    def test_django_conf(self):
        """
        Check that `reviews` is in `settings.INSTALLED_APPS`. STATIC_ROOT and STATICFILES_STORAGE should not be set.
        """
        self.assertIn('reviews', settings.INSTALLED_APPS)
        self.assertIsNone(settings.STATIC_ROOT)
        self.assertEquals(settings.STATICFILES_STORAGE, 'django.contrib.staticfiles.storage.StaticFilesStorage')

    def test_logo_get(self):
        """
        Test that the logo.png can be downloaded, and the content matches that on disk. This also checks the logo.png is
        in the right location and is being served using the static files finder.
        """
        response = urlopen(self.live_server_url + '/static/reviews/logo.png').read()
        with open(os.path.join(settings.BASE_DIR, 'reviews', 'static', 'reviews', 'logo.png'), 'rb') as f:
            self.assertEqual(response, f.read())

    def test_base_logo_display(self):
        """Test that the base template has no logo."""
        c = Client()
        resp = c.get('/')
        self.assertIn(b'<a class="navbar-brand" href="/">Book Review</a>', resp.content)

    def test_reviews_logo_display(self):
        """Test that the reviews page(s) have a logo set."""
        c = Client()
        resp = c.get('/books/')
        self.assertIn(b'<a class="navbar-brand" href="/"><img src="/static/reviews/logo.png"></a>', resp.content)

    def test_review_base_extends_main(self):
        """Test that the reviews base.html extends from the main base.html"""
        reviews_base = read_content(os.path.join(settings.BASE_DIR, 'reviews', 'templates', 'reviews', 'base.html'))
        self.assertTrue(reviews_base.startswith('{% extends \'base.html\' %}'))

    def test_reviews_templates_extend_reviews_base(self):
        """Test that the reviews templates extends the reviews base.html file."""
        book_detail_template = read_content(os.path.join(settings.BASE_DIR, 'reviews', 'templates', 'reviews',
                                                         'book_detail.html'))
        self.assertTrue(book_detail_template.startswith('{% extends \'reviews/base.html\' %}'))

        book_list_template = read_content(os.path.join(settings.BASE_DIR, 'reviews', 'templates', 'reviews',
                                                       'book_list.html'))
        self.assertTrue(book_list_template.startswith('{% extends \'reviews/base.html\' %}'))