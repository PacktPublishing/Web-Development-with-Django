from django import template
from reviews.models import Review

register = template.Library()

@register.inclusion_tag('book_list.html')
def book_list(username):
  """Render the list of books read by a user.

  :param: str username The username for whom the books should be fetched

  :return: dict of books read by user
  """
  reviews = Review.objects.filter(creator__username__contains=username)
  book_list = [review.book.title for review in reviews]
  return {'books_read': book_list}
  
