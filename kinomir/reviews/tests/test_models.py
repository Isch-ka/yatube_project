from django.test import TestCase
from django.contrib.auth import get_user_model
from reviews.models import Review, Genre

User = get_user_model()


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.genre = Genre.objects.create(
            name='Боевик',
            slug='boevik',
            description='Экшн фильмы'
        )
        self.review = Review.objects.create(
            movie_title='Тестовый фильм',
            director='Тестовый режиссёр',
            release_year=2020,
            text='Отличный фильм!',
            rating=8,
            author=self.user,
            genre=self.genre,
            is_approved=True
        )

    def test_review_creation(self):
        self.assertEqual(self.review.movie_title, 'Тестовый фильм')
        self.assertEqual(self.review.rating, 8)
        self.assertTrue(self.review.is_approved)

    def test_review_str_method(self):
        expected = 'Тестовый фильм (2020) - testuser'
        self.assertEqual(str(self.review), expected)


class GenreModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(
            name='Комедия',
            slug='comedy',
            description='Смешные фильмы'
        )

    def test_genre_creation(self):
        self.assertEqual(self.genre.name, 'Комедия')
        self.assertEqual(self.genre.slug, 'comedy')