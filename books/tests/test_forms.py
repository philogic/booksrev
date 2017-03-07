from django.core.exceptions import NON_FIELD_ERRORS
from django.test import TestCase
from books.factories import AuthorFactory, BookFactory
from books.forms import BookForm, ReviewForm


class ReviewFormTest(TestCase):
    def test_no_review(self):
        form = ReviewForm(data={
            'is_favourite': False,
        })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('review', code='required'))

    def test_review_too_short(self):
        form = ReviewForm(data={
            'is_favourite': False,
            'review': 'A test review'
        })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('review', code='min_length'))