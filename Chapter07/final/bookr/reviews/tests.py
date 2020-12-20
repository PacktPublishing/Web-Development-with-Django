import re

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.utils import timezone

from reviews.forms import ReviewForm
from reviews.models import Publisher, Book, Review


class Activity2Test(TestCase):
    def setUp(self):
        publisher_name = 'Test Edit Publisher'
        publisher_website = 'http://www.example.com/edit-publisher/'
        publisher_email = 'edit-publisher@example.com'
        self.publisher = Publisher.objects.create(name=publisher_name, website=publisher_website, email=publisher_email)
        Book.objects.create(title='Test Book', publication_date=timezone.now(), publisher=self.publisher, isbn=123456)

        User.objects.create(username='testuser', email='testuser@example.com')
        User.objects.create(username='testuser2', email='testuser2@example.com')

    def test_rating_field(self):
        """The rating field should be defined on the form manually."""
        form = ReviewForm()
        self.assertEquals(form.fields['rating'].min_value, 0)
        self.assertEquals(form.fields['rating'].max_value, 5)
        self.assertTrue(form.fields['rating'].required)

    def test_fields_and_labels_in_view(self):
        """"
        Test that fields and labels/headings exist in the rendered template.
        """
        c = Client()
        response = c.get('/books/1/reviews/new/')

        self.assertIsNotNone(re.search(r'<input type="hidden" name="csrfmiddlewaretoken" value="\w+">',
                                       response.content.decode('utf8')))

        self.assertIn(
            b'<label for="id_content">Content:</label> <textarea name="content" cols="40" rows="10" '
            b'required id="id_content">\n</textarea> <span class="helptext">The Review text.</span>',
            response.content)
        self.assertIn(
            b'<label for="id_rating">Rating:</label> <input type="number" name="rating" min="0" max="5" required '
            b'id="id_rating">', response.content)
        self.assertIn(b'<label for="id_creator">Creator:</label>', response.content)
        self.assertIn(b'<select name="creator" required id="id_creator">', response.content)
        self.assertIn(b'<option value="" selected>---------</option>', response.content)
        self.assertIn(b'<option value="1">testuser</option>', response.content)
        self.assertIn(b'<option value="2">testuser2</option>', response.content)
        self.assertNotIn(b'name="date_edited"', response.content)  # book should not be settable through form
        self.assertNotIn(b'name="book"', response.content)  # book should not be settable through form
        self.assertIn(b'<button type="submit" class="btn btn-primary">\n        Create\n    </button>',
                      response.content)

        self.assertIn(b'<p>For Book <em>Test Book (123456)</em></p>', response.content)

    def test_review_create(self):
        """Test review creation through the ReviewForm"""
        c = Client()
        review_content = 'A Great Book'
        review_rating = 3
        creator_id = 1

        response = c.post('/books/1/reviews/new/', {
            'content': review_content,
            'rating': review_rating,
            'creator': creator_id
        })
        review = Review.objects.get(pk=1)
        self.assertEquals(review.content, review_content)
        self.assertEquals(review.rating, review_rating)
        self.assertEquals(review.creator_id, creator_id)
        self.assertEquals(review.book_id, 1)
        self.assertIsNone(review.date_edited)

        # check redirect for the success message
        response = c.get(response['location'])

        condensed_content = re.sub(r'\s+', ' ', response.content.decode('utf8').replace('\n', ''))

        self.assertIn(
            '<div class="alert alert-success" role="alert"> Review for &quot;Test Book (123456)&quot; created. </div>',
            condensed_content)

    def test_review_no_create(self):
        """Test that no Review is created if the form is invalid."""
        self.assertEqual(Review.objects.all().count(), 0)
        c = Client()

        c.post('/books/1/reviews/new/', {
            'content': '',
            'rating': 6,
            'creator': 0
        })
        self.assertEqual(Review.objects.all().count(), 0)

    def test_review_book_mismatch(self):
        """It should not be possible to load a review unless it's for the right book."""
        b = Book.objects.create(title='Book2', publication_date=timezone.now(), publisher=self.publisher)
        Review.objects.create(content='Great.', rating=3, creator_id=1, book=b)

        c = Client()
        self.assertEquals(c.get('/books/1/').status_code, 200)
        self.assertEquals(c.get('/books/2/').status_code, 200)
        self.assertEquals(c.get('/books/2/reviews/1/').status_code, 200)
        self.assertEquals(c.get('/books/1/reviews/1/').status_code, 404)

    def test_review_edit(self):
        """
        Test editing a review, the initial form should have the values from the review being edited. Then no extra
        review should be created.
        """
        review_content = 'A real good book.'
        review_rating = 4

        Review.objects.create(content=review_content, rating=review_rating, creator_id=1, book_id=1)

        c = Client()

        response = c.get('/books/1/reviews/1/')

        self.assertIn(b'<input type="number" name="rating" value="4" min="0" max="5" required id="id_rating">',
                      response.content)
        self.assertIn(b'<option value="1" selected>', response.content)
        self.assertIn(b'<textarea name="content" cols="40" rows="10" required id="id_content">\nA real good book.'
                      b'</textarea>', response.content)
        self.assertIn(b'<button type="submit" class="btn btn-primary">\n        Save\n    </button>',
                      response.content)

        response = c.post('/books/1/reviews/1/', {
            'content': 'Changed my mind',
            'rating': 1,
            'creator': 2
        })

        review = Review.objects.get()
        self.assertEquals(review.content, 'Changed my mind')
        self.assertEquals(review.rating, 1)
        self.assertEquals(review.creator_id, 2)
        self.assertEquals(review.book_id, 1)
        # the messages will be on the redirected to page

        response = c.get(response['location'])

        condensed_content = re.sub(r'\s+', ' ', response.content.decode('utf8').replace('\n', ''))

        self.assertIn(
            '<div class="alert alert-success" role="alert"> Review for &quot;Test Book (123456)&quot; updated. </div>',
            condensed_content)

    def test_404_responses(self):
        """
        When trying to get a review for a book that does exist, or get a review that doesn't exist, we should get a 404.
        """
        c = Client()
        response = c.get('/books/123/reviews/new/')
        self.assertEquals(response.status_code, 404)

        response = c.get('/books/1/reviews/123/')
        self.assertEquals(response.status_code, 404)

    def test_add_review_link(self):
        """The add review link should display on the Book detail page."""
        c = Client()
        response = c.get('/books/1/')
        self.assertIn(b'<a class="btn btn-primary" href="/books/1/reviews/new/">Add Review</a>', response.content)

    def test_review_display(self):
        """We should see a link to edit a review after creating one."""
        Review.objects.create(content="Abc123", rating=2, creator_id=1, book_id=1)
        c = Client()
        response = c.get('/books/1/')
        self.assertIn(b'<a href="/books/1/reviews/1/">Edit Review</a>', response.content)
