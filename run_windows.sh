python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
cd kinomir
python manage.py migrate
python manage.py loaddata fixtures/kinomir_data.json
python manage.py runserver