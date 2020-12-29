from django.contrib import admin
from django.utils.translation import gettext as _
from reviews.models import Book

class BooksAdmin(admin.ModelAdmin):
  model = Book
  list_display = ('title', 'isbn', 'get_publisher')
  search_fields = ['title', 'publisher__name']

  def get_publisher(self, obj):
    return obj.publisher.name
  get_publisher.short_description = _("Publisher")
  
class BookrAdmin(admin.AdminSite):
  site_header = "Bookr Administration Portal"
  site_title = "Bookr Administration Portal"
  index_title = "Bookr Administration"

admin.site.register(Book, BooksAdmin)
