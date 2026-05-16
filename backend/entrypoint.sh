#!/bin/sh

echo "Waiting for DB..."

while ! nc -z db 3306; do
  sleep 2
done

echo "Port is open, waiting for MySQL..."

while ! python manage.py shell -c "from django.db import connections; connections['default'].cursor()" 2>/dev/null; do
  echo "DB not ready..."
  sleep 2
done

echo "DB is ready"

python manage.py migrate --noinput

exec python manage.py runserver 0.0.0.0:8000