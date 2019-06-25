release: python manage.py migrate
web: gunicorn flightapp.wsgi:application
worker: celery -A flightapp worker --beat -l info
