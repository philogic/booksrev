from django.test import TestCase
from django.urls import resolve,reverse
from books.factories import AuthorFactory, BookFactory, ReviewFactory
from books.views import list_books


class TestListBooks(TestCase):
    def test_list_books_url(self):
        url = resolve('/')
        self.assertEqual(url.func, list_books)

    def list_books_template(self):
        response = self.client.get(reverse(list_books))
        self.assertTemplateUsed(response, 'books/list.html')

    def list_books_with_reviews(self):
        author = AuthorFactory
        books_with_reviews = ReviewFactory.create_batch(2, authors=[author,])
        books_without_reviews = BookFactory.create_batch(4, authors=[author,])

        response = self.client.get(reverse(list_books))
        books = list(response.context['books'])

        self.assertEqual(books_with_reviews, books)
        self.assertHTMLNotEqual(books_without_reviews, books)
