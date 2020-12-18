from django.http import HttpResponse
from .models import Book


def welcome_view(request):
    message = f"<html><h1>Welcome to Bookr!</h1> <p>{Book.objects.count()} books and counting!</p></html>"
    return HttpResponse(message)
