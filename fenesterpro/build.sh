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
