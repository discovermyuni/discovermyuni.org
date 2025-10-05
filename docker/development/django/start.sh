#!/bin/sh
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Optionally create a superuser if env vars provided (safer than hardcoding)
# Provide DJANGO_SUPERUSER_EMAIL / DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD
if [ "${DJANGO_CREATE_SUPERUSER:-1}" = "1" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Ensuring superuser $DJANGO_SUPERUSER_USERNAME exists..."
  python manage.py shell << EOF
from django.contrib.auth import get_user_model
from django.core.management import call_command
User = get_user_model()
email = "$DJANGO_SUPERUSER_EMAIL"
username = "$DJANGO_SUPERUSER_USERNAME"
if not User.objects.filter(username=username).exists():
    print("Creating superuser", username)
    call_command('createsuperuser', '--noinput', username=username, email=email)
else:
    print("Superuser already exists: ", username)
EOF
fi

echo "Starting development server..."
exec python manage.py runserver 0.0.0.0:8000
