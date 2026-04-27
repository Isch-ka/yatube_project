from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from reviews.models import Review, Genre

User = get_user_model()


class StaticURLTests(TestCase):
    """Тестируем доступность страниц."""

    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        """Главная страница доступна."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_genres_list_page(self):
        """Страница списка жанров доступна."""
        response = self.guest_client.get(reverse('reviews:genres_list'))
        self.assertEqual(response.status_code, 200)

    def test_about_author_page(self):
        """Страница об авторе доступна."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_about_tech_page(self):
        """Страница о технологиях доступна."""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)


class ReviewViewsTest(TestCase):
    """Тестируем view-функции с данными."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser')
        self.genre = Genre.objects.create(
            name='Боевик',
            slug='action'
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

    def test_genre_page_accessible(self):
        """Страница жанра доступна."""
        response = self.client.get(
            reverse('reviews:genre_list', args=[self.genre.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_profile_page_accessible(self):
        """Страница профайла пользователя доступна."""
        response = self.client.get(
            reverse('reviews:profile', args=[self.user.username])
        )
        self.assertEqual(response.status_code, 200)

    def test_review_detail_page_accessible(self):
        """Страница отдельной рецензии доступна."""
        response = self.client.get(
            reverse('reviews:review_detail', args=[self.review.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_create_review_redirects_unauthorized(self):
        """Неавторизованный перенаправляется на страницу входа."""
        response = self.client.get(reverse('reviews:review_create'))
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_create_review_authorized(self):
        """Авторизованный может создать рецензию."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('reviews:review_create'))
        self.assertEqual(response.status_code, 200)

    def test_non_approved_review_not_shown(self):
        """Неодобренные рецензии не показываются на главной."""
        not_approved = Review.objects.create(
            movie_title='Скрытый фильм',
            director='Скрытый режиссёр',
            release_year=2023,
            text='Скрытая рецензия',
            rating=7,
            author=self.user,
            genre=self.genre,
            is_approved=False
        )
        response = self.client.get(reverse('reviews:index'))
        self.assertNotContains(response, 'Скрытый фильм')