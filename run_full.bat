@echo off
echo Создание виртуального окружения...
python -m venv venv

echo Активация окружения...
call venv\Scripts\activate.bat

echo Установка зависимостей...
pip install -r requirements.txt

cd kinomir

echo Выполнение миграций...
python manage.py migrate

echo Загрузка тестовых данных...
python manage.py loaddata fixtures/kinomir_data.json

echo Создание суперпользователя...
python manage.py createsuperuser

echo Запуск тестов...
python manage.py test

echo Запуск сервера...
python manage.py runserver

cmd /k