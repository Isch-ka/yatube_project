from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from reviews.forms import ReviewForm
from reviews.models import Review, Genre

User = get_user_model()


class ReviewFormTests(TestCase):
    """Тестируем форму ReviewForm."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        cls.genre = Genre.objects.create(
            name='Боевик',
            slug='action',
            description='Напряжённые сцены'
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_valid_form_creates_review(self):
        """Валидная форма создаёт новую рецензию."""
        reviews_count = Review.objects.count()
        
        form_data = {
            'movie_title': 'Новый фильм',
            'director': 'Новый режиссёр',
            'release_year': 2023,
            'text': 'Текст новой рецензии',
            'rating': 9,
            'genre': self.genre.id,
        }
        
        response = self.authorized_client.post(
            reverse('reviews:review_create'),
            data=form_data,
            follow=True
        )
        
        self.assertRedirects(response, reverse('reviews:profile', args=[self.user.username]))
        self.assertEqual(Review.objects.count(), reviews_count + 1)
        self.assertTrue(
            Review.objects.filter(
                movie_title='Новый фильм',
                director='Новый режиссёр',
                author=self.user
            ).exists()
        )

    def test_valid_form_without_genre_creates_review(self):
        """Валидная форма без жанра создаёт рецензию."""
        reviews_count = Review.objects.count()
        
        form_data = {
            'movie_title': 'Фильм без жанра',
            'director': 'Режиссёр',
            'release_year': 2022,
            'text': 'Текст рецензии без жанра',
            'rating': 7,
        }
        
        response = self.authorized_client.post(
            reverse('reviews:review_create'),
            data=form_data,
            follow=True
        )
        
        self.assertEqual(Review.objects.count(), reviews_count + 1)
        self.assertTrue(
            Review.objects.filter(
                movie_title='Фильм без жанра',
                genre__isnull=True
            ).exists()
        )

    def test_empty_text_invalid(self):
        """Пустой текст рецензии не проходит валидацию."""
        reviews_count = Review.objects.count()
        
        form_data = {
            'movie_title': 'Фильм',
            'director': 'Режиссёр',
            'release_year': 2023,
            'text': '',
            'rating': 8,
        }
        
        response = self.authorized_client.post(
            reverse('reviews:review_create'),
            data=form_data,
            follow=True
        )
        
        self.assertEqual(Review.objects.count(), reviews_count)
        self.assertFormError(response, 'form', 'text', 'Обязательное поле.')

    def test_empty_movie_title_invalid(self):
        """Пустое название фильма не проходит валидацию."""
        reviews_count = Review.objects.count()
        
        form_data = {
            'movie_title': '',
            'director': 'Режиссёр',
            'release_year': 2023,
            'text': 'Текст рецензии',
            'rating': 8,
        }
        
        response = self.authorized_client.post(
            reverse('reviews:review_create'),
            data=form_data,
            follow=True
        )
        
        self.assertEqual(Review.objects.count(), reviews_count)
        self.assertFormError(response, 'form', 'movie_title', 'Обязательное поле.')

    def test_invalid_release_year_too_old(self):
        """Слишком старый год выпуска не проходит валидацию."""
        reviews_count = Review.objects.count()
        
        form_data = {
            'movie_title': 'Древний фильм',
            'director': 'Древний режиссёр',
            'release_year': 1800,
            'text': 'Текст рецензии',
            'rating': 8,
        }
        
        response = self.authorized_client.post(
            reverse('reviews:review_create'),
            data=form_data,
            follow=True
        )
        
        self.assertEqual(Review.objects.count(), reviews_count)
        self.assertFormError(response, 'form', 'release_year', 'Год должен быть от 1888 до 2026')

    def test_invalid_release_year_future(self):
        """Год выпуска в будущем не проходит валидацию."""
        reviews_count = Review.objects.count()
        
        form_data = {
            'movie_title': 'Фильм будущего',
            'director': 'Режиссёр',
            'release_year': 2030,
            'text': 'Текст рецензии',
            'rating': 8,
        }
        
        response = self.authorized_client.post(
            reverse('reviews:review_create'),
            data=form_data,
            follow=True
        )
        
        self.assertEqual(Review.objects.count(), reviews_count)
        self.assertFormError(response, 'form', 'release_year', 'Год должен быть от 1888 до 2026')

    def test_edit_review_changes_data(self):
        """Редактирование рецензии изменяет данные."""
        review = Review.objects.create(
            movie_title='Старое название',
            director='Старый режиссёр',
            release_year=2020,
            text='Старый текст',
            rating=5,
            author=self.user,
            is_approved=True
        )
        
        form_data = {
            'movie_title': 'Новое название',
            'director': 'Новый режиссёр',
            'release_year': 2023,
            'text': 'Новый текст',
            'rating': 9,
            'genre': self.genre.id,
        }
        
        response = self.authorized_client.post(
            reverse('reviews:review_edit', args=[review.id]),
            data=form_data,
            follow=True
        )
        
        self.assertRedirects(response, reverse('reviews:profile', args=[self.user.username]))
        
        review.refresh_from_db()
        
        self.assertEqual(review.movie_title, 'Новое название')
        self.assertEqual(review.director, 'Новый режиссёр')
        self.assertEqual(review.release_year, 2023)
        self.assertEqual(review.text, 'Новый текст')
        self.assertEqual(review.rating, 9)
        self.assertEqual(review.genre, self.genre)

    def test_unauthorized_cannot_create_review(self):
        """Неавторизованный пользователь не может создать рецензию."""
        reviews_count = Review.objects.count()
        
        form_data = {
            'movie_title': 'Чужой фильм',
            'director': 'Чужой режиссёр',
            'release_year': 2023,
            'text': 'Текст чужой рецензии',
            'rating': 8,
        }
        
        guest_client = Client()
        response = guest_client.post(
            reverse('reviews:review_create'),
            data=form_data,
            follow=True
        )
        
        self.assertEqual(Review.objects.count(), reviews_count)
        self.assertRedirects(response, '/auth/login/?next=/create/')