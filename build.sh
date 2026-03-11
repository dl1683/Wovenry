#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# Seed admin superuser for demo environment
python manage.py shell -c "
from django.contrib.auth.models import User
from core.models import AllowedEmail
AllowedEmail.objects.get_or_create(email='admin@wovenry.com')
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@wovenry.com', 'admin123')
    print('Admin user created')
else:
    print('Admin user already exists')
"
