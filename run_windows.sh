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
    
    echo "Создание суперпользователя..."
    python manage.py createsuperuser
    
    echo "Запуск тестов..."
    python manage.py test
    
    cd ..
else
    echo "Активация существующего окружения..."
    source venv/Scripts/activate
fi

# Переход в папку проекта
cd kinomir

# Запуск сервера
echo "Запуск сервера..."
echo "Остановить сервер: Ctrl+C"
python manage.py runserver

# Запускаем новую оболочку, которая унаследует окружение
exec $SHELL