#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations to build the database
python manage.py migrate

# Collect static files for production styling
python manage.py collectstatic --no-input

# (Optional) Seed the database with demo data if it's empty
python manage.py seed_demo_data

# Create a superuser from environment variables (only if one doesn't exist)
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
if email and password and not User.objects.filter(email=email).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {email} created.')
else:
    print('Superuser already exists or env vars not set, skipping.')
"
