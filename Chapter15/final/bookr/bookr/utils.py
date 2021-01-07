import datetime

from django.db.models import Count
from reviews.models import Review


def get_books_read(username):
    """Get the list of books read by a user.

    :param: str username for whom the book records should be returned

    :return: list of dict of books read and date of posting the review
    """
    books = Review.objects.filter(creator__username__contains=username).all()
    return [{'title': book_read.book.title, 'completed_on': book_read.date_created} for book_read in books]


def get_books_read_by_month(username):
    """Get the books read by the user on per month basis.

    :param: str The username for which the books needs to be returned

    :return: dict of month wise books read
    """
    current_year = datetime.datetime.now().year
    books = Review.objects.filter(creator__username__contains=username,date_created__year=current_year).values('date_created__month').annotate(book_count=Count('book__title'))
    return books
