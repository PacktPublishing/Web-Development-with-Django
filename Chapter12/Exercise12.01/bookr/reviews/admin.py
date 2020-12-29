from django.contrib import admin

from .models import Book, Review

class BookAdmin(admin.ModelAdmin):
  model = Book
  list_display = ('title', 'isbn', 'get_publisher', 'publication_date')
  search_fields = ['title', 'publisher__name']

  def get_publisher(self, obj):
    return obj.publisher.name

admin.site.register(Book, BookAdmin)
admin.site.register(Review)
