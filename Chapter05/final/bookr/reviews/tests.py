import os
from urllib.request import urlopen

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client


def read_content(path):
    with open(path) as f:
        return f.read()


class Activity3Test(StaticLiveServerTestCase):
    """
    These tests use `StaticLiveServerTestCase` and `urlopen` since the normal `TestCase` uses a special server that does
    not serve static assets.
    """

    def test_django_conf(self):
        """
        Check that `reviews` is in `settings.INSTALLED_APPS` and that the static dir is set to <projectdir>/static.

        STATIC_ROOT and STATICFILES_STORAGE should not be set.
        """
        self.assertIn('reviews', settings.INSTALLED_APPS)
        self.assertEquals([settings.BASE_DIR + '/static'], settings.STATICFILES_DIRS)
        self.assertIsNone(settings.STATIC_ROOT)
        self.assertEquals(settings.STATICFILES_STORAGE, 'django.contrib.staticfiles.storage.StaticFilesStorage')

    def test_reviews_logo_get(self):
        """
        Test that the reviews logo.png can be downloaded, and the content matches that on disk. This also checks the
        logo.png is in the right location and is being served using the static files finder.
        """
        response = urlopen(self.live_server_url + '/static/reviews/logo.png').read()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_dir, 'static', 'reviews', 'logo.png'), 'rb') as f:
            self.assertEqual(response, f.read())

    def test_main_logo_get(self):
        """
        Test that the main logo.png can be downloaded, and the content matches that on disk. This also checks the
        logo.png is in the right location and is being served using the static files finder.
        """
        response = urlopen(self.live_server_url + '/static/logo.png').read()
        with open(os.path.join(settings.BASE_DIR, 'static', 'logo.png'), 'rb') as f:
            self.assertEqual(response, f.read())

    def test_main_css_get(self):
        """
        Test that the main.css can be downloaded, and the content matches that on disk. This also checks that main.css
        is in the right location and is being served using the static files finder.

        Since we have the contents of the file we can check it has the right rules too.
        """
        response = urlopen(self.live_server_url + '/static/main.css').read()

        with open(os.path.join(settings.BASE_DIR, 'static', 'main.css'), 'rb') as f:
            self.assertEqual(response, f.read())

        self.assertIn(b'.navbar', response)
        self.assertIn(b'.navbar-brand', response)
        self.assertIn(b'.navbar-brand > img', response)
        self.assertIn(b'body', response)
        self.assertIn(b'h1, h2, h3, h4, h5, h6', response)

    def test_base_html_content(self):
        """
        In the base HTML we should see: {% load static %}, CSS loaded with {% static %} template tag, fonts load CSS
        tag, main logo in brand block and no <style>...</style> tags.
        """
        base_template = read_content(os.path.join(settings.BASE_DIR, 'templates', 'base.html'))
        self.assertIn('{% load static %}', base_template)
        self.assertIn('<link rel="stylesheet" href="{% static \'main.css\' %}">', base_template)
        self.assertIn('<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Libre+Baskerville|'
                      'Source+Sans+Pro&display=swap">', base_template)
        self.assertIn(
            '<a class="navbar-brand" href="/">{% block brand %}<img src="{% static \'logo.png\' %}">{% endblock %}</a>',
            base_template)
        self.assertNotIn('<style>', base_template)
        self.assertNotIn('</style>', base_template)

    def test_base_logo_display(self):
        """Test that the base template has no logo."""
        c = Client()
        resp = c.get('/')
        self.assertIn(b'<a class="navbar-brand" href="/"><img src="/static/logo.png"></a>', resp.content)

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
