import datetime

from django.db.models import Count
from reviews.models import Review


def get_books_read_by_month(username):
    """Get the books read by the user on per month basis.

    :param: str The username for which the books needs to be returned

    :return: dict of month wise books read
    """
    current_year = datetime.datetime.now().year
    books = Review.objects.filter(creator__username__contains=username,date_created__year=current_year).values('date_created__month').annotate(book_count=Count('book__title'))
    return books
