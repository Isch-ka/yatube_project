#!/bin/bash
# Linux / Mac

echo "Создание виртуального окружения..."
python3 -m venv venv

echo "Активация окружения..."
source venv/bin/activate

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