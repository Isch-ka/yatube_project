from django.test import TestCase
from django.contrib.auth import get_user_model
from reviews.forms import ReviewForm
from reviews.models import Genre

User = get_user_model()


class ReviewFormTest(TestCase):
    """Тестируем форму ReviewForm."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        cls.genre = Genre.objects.create(
            name='Боевик',
            slug='action'
        )

    def test_valid_form_with_genre(self):
        """Проверяем валидную форму с жанром."""
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
        """Проверяем валидную форму без жанра."""
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
        """Пустой текст рецензии не проходит валидацию."""
        form_data = {
            'movie_title': 'Тестовый фильм',
            'director': 'Тестовый режиссёр',
            'release_year': 2020,
            'text': '',
            'rating': 8
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)

    def test_invalid_release_year_too_old(self):
        """Слишком старый год выпуска не проходит валидацию."""
        form_data = {
            'movie_title': 'Тестовый фильм',
            'director': 'Тестовый режиссёр',
            'release_year': 1800,
            'text': 'Текст рецензии',
            'rating': 8
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('release_year', form.errors)

    def test_invalid_release_year_future(self):
        """Год выпуска в будущем не проходит валидацию."""
        form_data = {
            'movie_title': 'Тестовый фильм',
            'director': 'Тестовый режиссёр',
            'release_year': 2030,
            'text': 'Текст рецензии',
            'rating': 8
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('release_year', form.errors)

    def test_invalid_rating(self):
        """Оценка вне диапазона 1-10 не проходит валидацию."""
        form_data = {
            'movie_title': 'Тестовый фильм',
            'director': 'Тестовый режиссёр',
            'release_year': 2020,
            'text': 'Текст рецензии',
            'rating': 15
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)