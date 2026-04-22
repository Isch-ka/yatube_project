python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
cd kinomir
python manage.py migrate
python manage.py runserver