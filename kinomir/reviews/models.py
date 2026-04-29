from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    """Жанр фильма"""
    name = models.CharField(max_length=100, verbose_name='Название жанра')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Review(models.Model):
    """Рецензия на фильм"""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]

    movie_title = models.CharField(max_length=200, verbose_name='Название фильма')
    director = models.CharField(max_length=100, verbose_name='Режиссёр')
    release_year = models.PositiveIntegerField(verbose_name='Год выпуска')
    text = models.TextField(verbose_name='Текст рецензии')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Оценка (1-10)')
    trailer_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на трейлер')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрено администратором')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Автор')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews', verbose_name='Жанр')
    image = models.ImageField('Постер фильма', upload_to='reviews/', blank=True, null=True)

    def __str__(self):
        return f'{self.movie_title} ({self.release_year}) - {self.author.username}'

    class Meta:
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'
        ordering = ['-pub_date']