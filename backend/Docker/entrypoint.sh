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

# -------------------------------------------------------------
# 3. キャッシュテーブル作成
# -------------------------------------------------------------
echo "🗄️  キャッシュテーブルを作成"
python manage.py createcachetable || true

echo "🌐 Django 開発サーバーを起動します"
python manage.py runserver 0.0.0.0:8000