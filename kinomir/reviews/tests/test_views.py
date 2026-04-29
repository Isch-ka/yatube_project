from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from reviews.models import Review, Genre

User = get_user_model()


class ReviewViewsTest(TestCase):
    """Тестируем view-функции: шаблоны и контекст."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        cls.genre = Genre.objects.create(
            name='Боевик',
            slug='action',
            description='Напряжённые сцены'
        )
        cls.review = Review.objects.create(
            movie_title='Тестовый фильм',
            director='Тестовый режиссёр',
            release_year=2020,
            text='Отличный фильм! Очень понравился.',
            rating=8,
            author=cls.user,
            genre=cls.genre,
            is_approved=True
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # ========== ТЕСТЫ ШАБЛОНОВ ==========

    def test_pages_uses_correct_template(self):
        """Проверяем, что страницы используют правильные шаблоны."""
        templates_pages_names = {
            'reviews/index.html': reverse('reviews:index'),
            'reviews/genres_list.html': reverse('reviews:genres_list'),
            'reviews/profile.html': reverse('reviews:profile', args=[self.user.username]),
            'reviews/review_detail.html': reverse('reviews:review_detail', args=[self.review.id]),
            'reviews/review_form.html': reverse('reviews:review_create'),
            'reviews/genre_list.html': reverse('reviews:genre_list', args=[self.genre.slug]),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # ========== ТЕСТЫ КОНТЕКСТА ==========

    def test_genre_list_page_show_correct_context(self):
        """Страница списка жанров передаёт правильный контекст."""
        response = self.authorized_client.get(reverse('reviews:genres_list'))
        self.assertIn('page_obj', response.context)
        self.assertIn('total_genres', response.context)

    def test_profile_page_show_correct_context(self):
        """Страница профайла передаёт правильный контекст."""
        response = self.authorized_client.get(
            reverse('reviews:profile', args=[self.user.username])
        )
        self.assertEqual(response.context['author'], self.user)
        self.assertIn('page_obj', response.context)
        self.assertIn('total_reviews', response.context)

    def test_review_detail_page_show_correct_context(self):
        """Страница рецензии передаёт правильный контекст."""
        response = self.authorized_client.get(
            reverse('reviews:review_detail', args=[self.review.id])
        )
        self.assertEqual(response.context['review'], self.review)
        self.assertEqual(response.context['total_reviews'], 1)

    def test_genre_reviews_page_show_correct_context(self):
        """Страница рецензий по жанру передаёт правильный контекст."""
        response = self.authorized_client.get(
            reverse('reviews:genre_list', args=[self.genre.slug])
        )
        self.assertEqual(response.context['genre'], self.genre)
        self.assertIn('page_obj', response.context)

    def test_home_page_contains_reviews(self):
        """Главная страница содержит список рецензий."""
        response = self.authorized_client.get(reverse('reviews:index'))
        self.assertIn('page_obj', response.context)

    # ========== ТЕСТЫ ОТОБРАЖЕНИЯ ==========

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
        response = self.authorized_client.get(reverse('reviews:index'))
        self.assertNotContains(response, 'Скрытый фильм')