from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, View
from .forms import ReviewForm
from .models import Author, Book

# Create your views here.
def list_books(request):
    """
    List only books that have reviews
    """

    books = Book.objects.exclude(date_reviewed__isnull=True).prefetch_related('authors')

    context = {
        'books': books,
    }

    return render(request, 'books/list.html', context)

class AuthorList(View):
    def get(self, request):

        authors = Author.objects.annotate(
            published_books = Count('books')
        ).filter(
            published_books__gt=0
        )


        context = {
            'authors': authors,
        }

        return render(request, "books/authors.html", context)


class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book.html'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'books/author.html'


def review_books(request):
    """
    List all of the books that we want to review.
    """
    books = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')

    context = {
        'books': books,
    }

    return render(request, "books/list-to-review.html", context)


def review_book(request, pk):
    """
    Review an individual book
    """
    book = get_object_or_404(Book, pk=pk)
    form = ReviewForm

    context = {
        'book': book,
        'form': form,
    }

    return render(request, "books/review-book.html", context)
