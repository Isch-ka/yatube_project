#!/bin/bash
# Windows (Git Bash)

echo "Создание виртуального окружения..."
python -m venv venv

echo "Активация окружения..."
source venv/Scripts/activate

echo "Установка зависимостей..."
pip install -r requirements.txt

echo "Переход в папку проекта..."
cd kinomir

echo "Выполнение миграций..."
python manage.py migrate

echo "Загрузка тестовых данных..."
python manage.py loaddata fixtures/kinomir_data.json

echo "Создание суперпользователя:"
python manage.py createsuperuser

echo "Запуск тестов..."
python manage.py test

echo "Запуск сервера..."
python manage.py runserver