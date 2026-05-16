#!/bin/sh

echo "Waiting for DB..."

# ポート開くまで待つ
while ! nc -z db 3306; do
  sleep 2
done

echo "MySQL port is open"

# ちょい待つ（←これ超重要）
sleep 5

echo "Running migrations..."

python manage.py migrate --noinput

exec python manage.py runserver 0.0.0.0:8000