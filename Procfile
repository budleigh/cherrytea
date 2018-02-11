release: python manage.py migrate --no-input
web: gunicorn cherrytea.wsgi --log-file -
clock: python clock.py
