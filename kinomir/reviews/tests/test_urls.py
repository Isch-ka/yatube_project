from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from reviews.models import Review, Genre

User = get_user_model()


class StaticURLTests(TestCase):
    """Тестируем доступность статических страниц."""

    def setUp(self):
        self.guest_client = Client()

    def test_homepage_accessible(self):
        """Главная страница доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_genres_list_accessible(self):
        """Страница списка жанров доступна любому."""
        response = self.guest_client.get(reverse('reviews:genres_list'))
        self.assertEqual(response.status_code, 200)

    def test_about_author_accessible(self):
        """Страница об авторе доступна любому."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_about_tech_accessible(self):
        """Страница о технологиях доступна любому."""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)

    def test_non_existent_page_404(self):
        """Несуществующая страница возвращает 404."""
        response = self.guest_client.get('/non-existent-page/')
        self.assertEqual(response.status_code, 404)


class TaskURLTests(TestCase):
    """Тестируем URL с авторизацией."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        cls.genre = Genre.objects.create(
            name='Боевик',
            slug='action'
        )
        cls.review = Review.objects.create(
            movie_title='Тестовый фильм',
            director='Тестовый режиссёр',
            release_year=2020,
            text='Отличный фильм!',
            rating=8,
            author=cls.user,
            genre=cls.genre,
            is_approved=True
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_review_redirects_anonymous(self):
        """Неавторизованный перенаправляется на страницу входа."""
        response = self.guest_client.get(reverse('reviews:review_create'))
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_create_review_accessible_authorized(self):
        """Авторизованный может создать рецензию."""
        response = self.authorized_client.get(reverse('reviews:review_create'))
        self.assertEqual(response.status_code, 200)

    def test_review_edit_redirects_anonymous(self):
        """Неавторизованный не может редактировать рецензию."""
        response = self.guest_client.get(
            reverse('reviews:review_edit', args=[self.review.id])
        )
        self.assertRedirects(
            response, 
            f'/auth/login/?next=/reviews/{self.review.id}/edit/'
        )

    def test_review_edit_accessible_for_author(self):
        """Автор может редактировать свою рецензию."""
        response = self.authorized_client.get(
            reverse('reviews:review_edit', args=[self.review.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_profile_page_accessible(self):
        """Страница профайла доступна."""
        response = self.guest_client.get(
            reverse('reviews:profile', args=[self.user.username])
        )
        self.assertEqual(response.status_code, 200)