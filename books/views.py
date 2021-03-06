from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, View
from django.views.generic.edit import CreateView
from .forms import ReviewForm, BookForm
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


class ReviewList(View):

    """
    List all of the books that we want to review.
    """
    def get(self, request):
        books = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')

        context = {
            'books': books,
            'form': BookForm,
        }

        return render(request, "books/list-to-review.html", context)

    def post(self, request):
        form = BookForm(request.POST)
        books = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')

        if form.is_valid():
            form.save()
            return redirect('review-books')

        context = {
            'form': form,
            'books': books,
        }

        return render(request, "books/list-to-review.html", context)

@login_required
def review_book(request, pk):
    """
    Review an individual book
    """
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            book.is_favourite = form.cleaned_data['is_favourite']
            book.review = form.cleaned_data['review']
            book.reviewed_by = request.user
            book.save()

            return redirect('review-books')
    else:
        form = ReviewForm

    context = {
        'book': book,
        'form': form,
    }

    return render(request, "books/review-book.html", context)


class CreateAuthor(CreateView):
    model = Author
    fields = ['name',]
    template_name = 'books/create-author.html'

    def get_success_url(self):
        return reverse('review-books')
