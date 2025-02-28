#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Check if the superuser exists, and create it if not
echo "Checking for superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()
if not User.objects.filter(email='admin@example.com').exists():
    print("Creating superuser...")
    call_command('createsuperuser', '--noinput', '--email', 'admin@example.com')
EOF

# Start the development server
echo "Starting development server..."
python manage.py runserver 0.0.0.0:8000
