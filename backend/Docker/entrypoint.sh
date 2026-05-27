#!/usr/bin/env bash
set -e

echo "🚀 Django application 起動開始"

echo "⏳ MySQL接続を確認します ${DB_HOST}:${DB_PORT}..."

DB_PORT=${DB_PORT:-3306}
DB_READY=false

for i in {1..10}; do
  if python - <<'PYCODE'
import os, sys, socket

db_host = os.environ.get("DB_HOST", "db")
db_port = int(os.environ.get("DB_PORT", "3306"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)

try:
    s.connect((db_host, db_port))
    s.close()
    print(f"✅ MySQL TCP接続成功 {db_host}:{db_port}")
    sys.exit(0)
except Exception:
    print(f"⚠️ MySQL TCP接続失敗 {db_host}:{db_port}")
    sys.exit(1)
PYCODE
  then
    DB_READY=true
    break
  fi

  echo "⏳ MySQL 接続再トライ ($i/10)"
  sleep 3
done

if [ "$DB_READY" != "true" ]; then
  echo "❌ MySQLに接続できませんでした。起動を中止します。"
  exit 1
fi

echo "📦 migrate"
python manage.py migrate --noinput

echo "🌱 seed_foods"
python manage.py seed_foods || true

if [ "${CREATE_SUPERUSER:-false}" = "true" ]; then
  echo "👤 superuser 作成確認"
  python manage.py shell <<PYCODE
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ superuser created")
else:
    print("ℹ️ superuser skipped")
PYCODE
fi

echo "📁 collectstatic"
python manage.py collectstatic --noinput

echo "🎯 gunicorn 起動"
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000