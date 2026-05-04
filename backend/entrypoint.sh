#!/bin/sh

echo "Waiting for DB..."

while ! nc -z db 3306; do
  sleep 2
done

echo "DB is ready"

python manage.py migrate --noinput

exec python manage.py runserver 0.0.0.0:8000