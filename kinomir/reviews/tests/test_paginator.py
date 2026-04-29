from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from reviews.models import Review, Genre

User = get_user_model()


class PaginatorViewsTest(TestCase):
    """Тестируем пагинатор."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        cls.genre = Genre.objects.create(
            name='Боевик',
            slug='action'
        )
        # Создаём 15 рецензий для проверки пагинации
        for i in range(15):
            Review.objects.create(
                movie_title=f'Фильм {i}',
                director=f'Режиссёр {i}',
                release_year=2020 + i % 5,
                text=f'Текст рецензии {i}',
                rating=5 + i % 5,
                author=cls.user,
                genre=cls.genre,
                is_approved=True
            )

    def setUp(self):
        self.client = Client()

    def test_first_page_contains_ten_records(self):
        """На первой странице должно быть 10 рецензий."""
        response = self.client.get(reverse('reviews:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_five_records(self):
        """На второй странице должно быть 5 рецензий."""
        response = self.client.get(reverse('reviews:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 5)

    def test_paginator_has_correct_number_of_pages(self):
        """Пагинатор имеет правильное количество страниц."""
        response = self.client.get(reverse('reviews:index'))
        self.assertEqual(response.context['page_obj'].paginator.num_pages, 2)