from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from reviews.models import Review, Genre

User = get_user_model()


class SearchTest(TestCase):
    """Тестируем поиск."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='alex_movie',
            first_name='Алексей',
            last_name='Смирнов'
        )
        self.genre = Genre.objects.create(name='Боевик', slug='action')
        Review.objects.create(
            movie_title='Джон Неделя 4',
            director='Чад Стахелски',
            release_year=2023,
            text='Отличный боевик про киллера',
            rating=9,
            author=self.user,
            genre=self.genre,
            is_approved=True
        )

    def test_search_by_movie_title(self):
        """Поиск по названию фильма работает."""
        response = self.client.get(reverse('reviews:index'), {'q': 'Джон'})
        self.assertContains(response, 'Джон Неделя 4')

    def test_search_by_director(self):
        """Поиск по режиссёру работает."""
        response = self.client.get(reverse('reviews:index'), {'q': 'Чад'})
        self.assertContains(response, 'Джон Неделя 4')

    def test_search_by_author_username(self):
        """Поиск по логину автора работает."""
        response = self.client.get(reverse('reviews:index'), {'q': 'alex'})
        self.assertContains(response, 'Джон Неделя 4')

    def test_search_by_author_first_name(self):
        """Поиск по имени автора работает."""
        response = self.client.get(reverse('reviews:index'), {'q': 'Алексей'})
        self.assertContains(response, 'Джон Неделя 4')