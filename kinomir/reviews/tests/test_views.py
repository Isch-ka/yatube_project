from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from reviews.models import Review, Genre

User = get_user_model()


class ReviewViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser')
        self.genre = Genre.objects.create(
            name='Боевик',
            slug='boevik'
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

    def test_index_page_accessible(self):
        response = self.client.get(reverse('reviews:index'))
        self.assertEqual(response.status_code, 200)

    def test_genre_page_accessible(self):
        response = self.client.get(
            reverse('reviews:genre_list', args=[self.genre.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_create_review_redirects_unauthorized(self):
        response = self.client.get(reverse('reviews:review_create'))
        self.assertRedirects(response, '/auth/login/?next=/create/')