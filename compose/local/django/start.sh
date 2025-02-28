#!/bin/sh

set -o errexit

python manage.py migrate
python manage.py createsuperuser --no-input --email admin@example.com
python manage.py runserver 0.0.0.0:8000
