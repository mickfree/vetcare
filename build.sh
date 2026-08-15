#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py check

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser --noinput

python manage.py shell -c "import os; from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.filter(username=os.environ['DJANGO_SUPERUSER_USERNAME']).update(role='ADMIN', is_staff=True, is_superuser=True, is_active=True)"