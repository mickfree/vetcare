#!/usr/bin/env bash
set -o errexit

python manage.py check

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py makemigrations

python manage.py migrate