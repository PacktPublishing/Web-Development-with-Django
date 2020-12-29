import os

from django.conf import settings
from django.test import TestCase, Client
from django.utils import timezone

from reviews.models import Book, Publisher


class Activity2Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        p = Publisher.objects.create(name='Test Publisher')
        Book.objects.create(title='Test Book', publication_date=timezone.now(), publisher=p)

    def test_book_detail_media_display(self):
        """
        When we first view a book we should not see a cover image or link to sample. But if we upload these, they should
        then be displayed on the book detail page.
        """
        cover_filename = 'machine-learning-for-algorithmic-trading.png'
        cover_save_path = os.path.join(settings.MEDIA_ROOT, 'book_covers', cover_filename)

        sample_filename = 'machine-learning-for-trading.pdf'
        sample_save_path = os.path.join(settings.MEDIA_ROOT, 'book_samples', sample_filename)

        cover_img = b'<img src="/media/book_covers/machine-learning-for-algorithmic-trading.png">'
        sample_link = b'<a href="/media/book_samples/machine-learning-for-trading.pdf">Download</a>'

        c = Client()
        resp = c.get('/books/1/')

        self.assertIn(b'<a class="btn btn-primary" href="/books/1/media/">Media</a>', resp.content)

        # check the cover image and sample link aren't in the initial HTML
        self.assertNotIn(cover_img, resp.content)
        self.assertNotIn(sample_link, resp.content)

        try:
            with open(os.path.join(settings.BASE_DIR, 'fixtures', cover_filename), 'rb') as cover_fp:
                with open(os.path.join(settings.BASE_DIR, 'fixtures', sample_filename), 'rb') as sample_fp:
                    c.post('/books/1/media/', {'cover': cover_fp, 'sample': sample_fp})
        finally:
            if os.path.exists(cover_save_path):
                os.unlink(cover_save_path)

            if os.path.exists(sample_save_path):
                os.unlink(sample_save_path)

        resp = c.get('/books/1/')

        # check the cover image and sample link are in the HTML after uploading the media
        self.assertIn(cover_img, resp.content)
        self.assertIn(sample_link, resp.content)
