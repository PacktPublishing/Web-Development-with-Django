from rest_framework import generics

from .models import Book
from .serializers import BookSerializer


class AllBooks(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
