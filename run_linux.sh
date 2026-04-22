python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd kinomir
python manage.py migrate
python manage.py runserver