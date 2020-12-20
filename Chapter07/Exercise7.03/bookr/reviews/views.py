from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PublisherForm, SearchForm
from .models import Book, Contributor, Publisher
from .utils import average_rating


def index(request):
    return render(request, "base.html")


def book_search(request):
    search_text = request.GET.get("search", "")
    form = SearchForm(request.GET)
    books = set()
    if form.is_valid() and form.cleaned_data["search"]:
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"
        if search_in == "title":
            books = Book.objects.filter(title__icontains=search)
        if search_in == "title":
            books = Book.objects.filter(title__icontains=search)
        else:
            fname_contributors = \
                Contributor.objects.filter(first_names__icontains=search)

            for contributor in fname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

        lname_contributors = \
            Contributor.objects.filter(last_names__icontains=search)

        for contributor in lname_contributors:
            for book in contributor.book_set.all():
                books.add(book)

    return render(request, "reviews/search-results.html", {"form": form, "search_text": search_text, "books": books})


def book_list(request):
    books = Book.objects.all()
    books_with_reviews = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        books_with_reviews.append({"book": book, "book_rating": book_rating, "number_of_reviews": number_of_reviews})

    context = {
        "book_list": books_with_reviews
    }
    return render(request, "reviews/book_list.html", context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {
            "book": book,
            "book_rating": book_rating,
            "reviews": reviews
        }
    else:
        context = {
            "book": book,
            "book_rating": None,
            "reviews": None
        }
    return render(request, "reviews/book_detail.html", context)


def publisher_edit(request, pk=None):
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None

    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(request, "Publisher \"{}\" was created.".format(updated_publisher))
            else:
                messages.success(request, "Publisher \"{}\" was updated.".format(updated_publisher))

            return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)

    return render(request, "form-example.html", {"method": request.method, "form": form})
