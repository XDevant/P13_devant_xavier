#!/bin/sh

set -e

whoami

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py loaddata db.json && rm db.json || true
gunicorn --env DJANGO_SETTINGS_MODULE=oc-lettings.settings oc-lettings.wsgi:application --bind 0.0.0.0:"$PORT"
