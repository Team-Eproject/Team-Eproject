#!/usr/bin/env bash
set -e # エラーが発生したら即座に終了
echo "🚀 Django application 起動開始"

# 依存関係適用（必要なら）
python -m pip install --upgrade pip >/dev/null 2>&1 || true

# -------------------------------------------------------------
# 1. MySQLの準備待ち
# -------------------------------------------------------------
echo "⏳ MySQL接続を開始します $DB_HOST:$DB_PORT..."

DB_PORT=${DB_PORT:-3306}

# MySQL接続待機（最大6秒）
for i in {1..3}; do
  if python - <<'PYCODE'
import os, sys, socket

db_host = os.environ.get("DB_HOST", "db")
db_port = int(os.environ.get("DB_PORT", "3306"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)

try:
    s.connect((db_host, db_port))
    s.close()
    print(f"✅ MySQL TCP接続成功しました {db_host}:{db_port}")
    sys.exit(0)
except Exception as e:
    print(f"⚠️ MySQL TCP接続失敗しました {db_host}:{db_port}")
    sys.exit(1)
PYCODE
  then
    break
  fi
  echo "⏳ MySQL 接続失敗 再トライ (attempt $i/3)"
  sleep 2
done

echo "✅ MySQL 接続完了"

PROJECT_NAME=${DJANGO_PROJECT_NAME:-config}

# プロジェクトが無ければ自動作成
if [ ! -f "manage.py" ]; then
  echo "manage.py not found. Creating Django project '${PROJECT_NAME}' ..."
  django-admin startproject "$PROJECT_NAME" .
fi

# Django 環境変数をロード
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# -------------------------------------------------------------
# 2. データベースマイグレーション
# -------------------------------------------------------------
echo "📦 マイグレーションを開始します"
python manage.py migrate --noinput

echo "🌱 初期データを作成します"
python manage.py seed_foods

# -------------------------------------------------------------
# 3. キャッシュテーブル作成
# -------------------------------------------------------------
echo "🗄️  キャッシュテーブルを作成"
python manage.py createcachetable || true

echo "🌐 Django 開発サーバーを起動します"
python manage.py runserver 0.0.0.0:8000

# -------------------------------------------------------------
# スーパーユーザーの作成（初回のみ）
# -------------------------------------------------------------
if [ "${CREATE_SUPERUSER:-false}" = "true" ]; then
  echo "👤 スーパーユーザーの登録を確認中、未登録なら自動作成します"
  python manage.py shell <<PYCODE
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ スーパーユーザー '{username}' 作成完了")
elif not password:
    print("⚠️  パスワードが設定されていません")
else:
    print(f"ℹ️  このスーパーユーザー '{username}' は既に登録されています")
PYCODE
fi

# -------------------------------------------------------------
# 静的ファイルの収集（S3へアップロード）本番時にコメント解除
# -------------------------------------------------------------
# echo "📁 静的ファイルを収集してS3にアップロード"
# python manage.py collectstatic --noinput --clear

# -------------------------------------------------------------
# Gunicorn起動 本番時にコメント解除
# -------------------------------------------------------------
#echo "🎯 Gunicorn起動します"
#exec gunicorn config.wsgi:application \
#  --config /app/Docker/gunicorn.conf.py \
#  --log-file - \
#  --error-logfile - \