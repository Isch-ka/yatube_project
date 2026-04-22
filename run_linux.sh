#!/bin/bash
# Linux / Mac

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd kinomir
python manage.py migrate
python manage.py loaddata fixtures/kinomir_data.json

echo "Создание суперпользователя:"
python manage.py createsuperuser

python manage.py runserver