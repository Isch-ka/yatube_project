from django.test import TestCase
from django.contrib.auth import get_user_model
from reviews.forms import ReviewForm
from reviews.models import Genre

User = get_user_model()


class ReviewFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.genre = Genre.objects.create(
            name='Боевик',
            slug='boevik'
        )

    def test_valid_form_with_genre(self):
        form_data = {
            'movie_title': 'Тестовый фильм',
            'director': 'Тестовый режиссёр',
            'release_year': 2020,
            'text': 'Текст рецензии',
            'rating': 8,
            'genre': self.genre.id
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_form_without_genre(self):
        form_data = {
            'movie_title': 'Тестовый фильм',
            'director': 'Тестовый режиссёр',
            'release_year': 2020,
            'text': 'Текст рецензии',
            'rating': 8
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_text_invalid(self):
        form_data = {'text': ''}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())