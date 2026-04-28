#!/bin/bash

# Создание и настройка (только если venv не существует)
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python -m venv venv
    
    echo "Активация окружения..."
    source venv/Scripts/activate
    
    echo "Установка зависимостей..."
    pip install -r requirements.txt
    
    cd kinomir
    
    echo "Выполнение миграций..."
    python manage.py migrate
    
    echo "Загрузка тестовых данных..."
    python manage.py loaddata fixtures/kinomir_data.json
    
    echo "Создание суперпользователя:"
    python manage.py createsuperuser
    
    echo "Запуск тестов..."
    python manage.py test
    
    cd ..
fi

# Активация окружения и переход в проект
source venv/Scripts/activate
cd kinomir

# Запуск новой оболочки с окружением
exec bash