#!/usr/bin/env bash

# =========================================================
# entrypoint.sh
# Djangoコンテナ起動時に最初に実行される処理
# =========================================================

set -e

echo "🚀 Django application 起動開始"


# =========================================================
# 0. 環境変数の初期値
# =========================================================

# DB_HOSTが未指定ならdocker-compose開発用のdbを使う
DB_HOST="${DB_HOST:-db}"

# DB_PORTが未指定ならMySQL標準ポート3306を使う
DB_PORT="${DB_PORT:-3306}"

# DJANGO_ENVが未指定なら開発環境として扱う
DJANGO_ENV="${DJANGO_ENV:-development}"


# =========================================================
# 1. MySQL / RDS の起動待ち
# =========================================================

echo "⏳ DB接続確認を開始します: ${DB_HOST}:${DB_PORT}"

# 最大30回、2秒間隔でDBへのTCP接続を確認する
# 開発環境のMySQLコンテナ、本番環境のRDSどちらにも対応
for i in {1..30}; do
  if python - <<PYCODE
import os
import socket
import sys

db_host = os.environ.get("DB_HOST", "db")
db_port = int(os.environ.get("DB_PORT", "3306"))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)

try:
    sock.connect((db_host, db_port))
    sock.close()
    print(f"✅ DB TCP接続成功: {db_host}:{db_port}")
    sys.exit(0)
except Exception:
    print(f"⚠️ DB TCP接続失敗: {db_host}:{db_port}")
    sys.exit(1)
PYCODE
  then
    break
  fi

  echo "⏳ DB接続待ち... attempt ${i}/30"
  sleep 2
done


# =========================================================
# 2. DBマイグレーション
# =========================================================

echo "📦 マイグレーションを実行します"

# DBテーブルを最新状態にする
python manage.py migrate --noinput


# =========================================================
# 3. 初期データ投入
# =========================================================

echo "🌱 初期食品データを作成します"

# seed_foodsはget_or_createを使っているため、基本的には再実行しても重複しにくい
# 失敗してもアプリ起動自体は止めたくない場合は || true を付ける
python manage.py seed_foods || true


# =========================================================
# 4. キャッシュテーブル作成
# =========================================================

echo "🗄️ キャッシュテーブルを確認します"

# 既に存在している場合はエラーになることがあるため、失敗しても続行
python manage.py createcachetable || true


# =========================================================
# 5. スーパーユーザー自動作成
# =========================================================

if [ "${CREATE_SUPERUSER:-false}" = "true" ]; then
  echo "👤 スーパーユーザーを確認します"

  python manage.py shell <<PYCODE
from django.contrib.auth import get_user_model
import os

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if not password:
    print("⚠️ DJANGO_SUPERUSER_PASSWORD が未設定のため作成しません")
elif User.objects.filter(username=username).exists():
    print(f"ℹ️ スーパーユーザー '{username}' は既に存在します")
else:
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
    print(f"✅ スーパーユーザー '{username}' を作成しました")
PYCODE
fi


# =========================================================
# 6. staticファイル収集
# =========================================================

if [ "${COLLECTSTATIC:-false}" = "true" ]; then
  echo "📁 collectstaticを実行します"

  # USE_S3=1の場合はS3のstatic配下へアップロードされる
  # USE_S3=0の場合はSTATIC_ROOTへ集約される
  python manage.py collectstatic --noinput
fi


# =========================================================
# 7. アプリ起動
# =========================================================

if [ "${DJANGO_ENV}" = "production" ]; then
  echo "🎯 本番モード: Gunicornで起動します"

  # 本番ではrunserverではなくGunicornを使う
  exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --timeout "${GUNICORN_TIMEOUT:-120}" \
    --access-logfile - \
    --error-logfile -
else
  echo "🌐 開発モード: Django runserverで起動します"

  # 開発では自動リロードが効くrunserverを使う
  exec python manage.py runserver 0.0.0.0:8000
fi