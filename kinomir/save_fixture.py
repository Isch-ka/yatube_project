import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kinomir.settings')
django.setup()

from django.core import serializers
from django.contrib.auth import get_user_model
from reviews.models import Genre, Review

User = get_user_model()

# Собираем все данные (кроме суперпользователя)
data = list(User.objects.filter(is_superuser=False)) + list(Genre.objects.all()) + list(Review.objects.all())

# Сохраняем в UTF-8
with open('fixtures/kinomir_data.json', 'w', encoding='utf-8') as f:
    serializers.serialize('json', data, indent=2, ensure_ascii=False, stream=f)

print("✅ Фикстура сохранена в fixtures/kinomir_data.json (UTF-8)")