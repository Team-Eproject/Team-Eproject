import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# 基本設定
# =========================================================

# SECRET_KEYは本番では必ず.envから読み込む
# dev-secret-keyは開発用の仮値
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

# DEBUG=1なら開発モード、DEBUG=0なら本番モード
DEBUG = os.getenv("DEBUG", "1") == "1"

# Djangoの実行環境を判定するための変数
# development / production などを.envで指定する
DJANGO_ENV = os.getenv("DJANGO_ENV", "development")

# カンマ区切りで複数のホストを.envから受け取る
# 例: ALLOWED_HOSTS=localhost,127.0.0.1,example.com
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "localhost,127.0.0.1"
).split(",")

# 主キーのデフォルト型
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================================================
# アプリ設定
# =========================================================

INSTALLED_APPS = [
    # Django標準アプリ
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 外部ライブラリ
    "rest_framework",
    "django_filters",
    "corsheaders",

    # S3保存用
    # django-storagesを使ってS3へstatic/mediaを保存する
    "storages",

    # 自作アプリ
    "apps.users",
    "apps.foods",
    "apps.shopping_memos",
]


# =========================================================
# ミドルウェア
# =========================================================

MIDDLEWARE = [
    # CORS設定を先に通す
    "corsheaders.middleware.CorsMiddleware",

    # HTTPSやセキュリティ関連
    "django.middleware.security.SecurityMiddleware",

    # セッション管理
    "django.contrib.sessions.middleware.SessionMiddleware",

    # 共通処理
    "django.middleware.common.CommonMiddleware",

    # CSRF対策
    "django.middleware.csrf.CsrfViewMiddleware",

    # ログインユーザー判定
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # メッセージ機能
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "config.urls"


# =========================================================
# テンプレート設定
# =========================================================

TEMPLATES = [
    {
        # アプリ画面ではJinja2を使用
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": False,
        "OPTIONS": {
            "environment": "config.jinja2.environment",
        },
    },
    {
        # Django管理画面用にDjango Templatesも残す
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# =========================================================
# データベース設定
# =========================================================

DATABASES = {
    "default": {
        # MySQLを使用
        "ENGINE": "django.db.backends.mysql",

        # DB名・ユーザー・パスワードは.envから読む
        "NAME": os.getenv("MYSQL_DATABASE"),
        "USER": os.getenv("MYSQL_USER"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD"),

        # 開発環境ではdb、本番環境ではRDSエンドポイントを指定
        "HOST": os.getenv("DB_HOST", "db"),
        "PORT": os.getenv("DB_PORT", "3306"),

        # 本番で接続が不安定な場合に備えて接続を再利用
        "CONN_MAX_AGE": int(os.getenv("DB_CONN_MAX_AGE", "60")),
    }
}


# =========================================================
# 認証設定
# =========================================================

# apps.users.UserをDjangoのユーザーモデルとして使う
AUTH_USER_MODEL = "users.User"

# ハッカソン中は簡易化のため空でもOK
# 本番品質を上げるなら後で有効化する
AUTH_PASSWORD_VALIDATORS = []


# =========================================================
# 言語・タイムゾーン
# =========================================================

LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True

# DBに日本時間で保存したい場合はFalse
# AWS運用でUTC統一したい場合はTrueも検討
USE_TZ = False


# =========================================================
# Static / Media 基本設定
# =========================================================

# static: CSS / JS / ロゴなど
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# media: ユーザーがアップロードした画像など
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# =========================================================
# S3設定
# =========================================================

# USE_S3=1 のときだけS3を使う
# 開発環境では0、本番環境では1にする想定
USE_S3 = os.getenv("USE_S3", "0") == "1"

if USE_S3:
    # S3バケット名
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")

    # AWSリージョン
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "ap-northeast-1")

    # S3のカスタムドメイン
    # 例: your-bucket.s3.ap-northeast-1.amazonaws.com
    AWS_S3_CUSTOM_DOMAIN = os.getenv(
        "AWS_S3_CUSTOM_DOMAIN",
        f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
    )

    # 署名付きURLを使わず、公開URLとして表示する設定
    # バケットを非公開にする場合はCloudFront構成に変更する
    AWS_QUERYSTRING_AUTH = os.getenv("AWS_QUERYSTRING_AUTH", "0") == "1"

    # ACLはS3側のバケットポリシー/IAMで管理する
    AWS_DEFAULT_ACL = None

    # 同名ファイルが上書きされにくいようにする
    AWS_S3_FILE_OVERWRITE = False

    # S3にアップロードしたstatic/mediaのURL
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

    # Django 5.2系ではSTORAGESで保存先を指定する
    STORAGES = {
        # ImageField/FileFieldの保存先
        # Food.imageやFoodTemplate.imageがS3のmedia配下に保存される
        "default": {
            "BACKEND": "config.strage_backends.MediaStorage",
        },

        # collectstaticで集めたCSS/JS/画像の保存先
        "staticfiles": {
            "BACKEND": "config.strage_backends.StaticStorage",
        },
    }

else:
    # 開発環境ではローカル保存
    STORAGES = {
        "default": {
            "BACKEND": "config.storage_backends.MediaStorage",
        },
        "staticfiles": {
            "BACKEND": "config.storage_backends.StaticStorage",
        },
    }


# =========================================================
# DRF設定
# =========================================================

REST_FRAMEWORK = {
    # セッション認証を使う
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}


# =========================================================
# CORS / CSRF設定
# =========================================================

# 開発時にVS Code Live Serverなどからアクセスする場合
CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://127.0.0.1:5500,http://localhost:5500"
).split(",")

# 本番でHTTPSドメインを使う場合
# 例: CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
CSRF_TRUSTED_ORIGINS = [
    origin
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin
]


# =========================================================
# HTTPS / Cookie設定
# =========================================================

if DJANGO_ENV == "production":
    # ALBやリバースプロキシ配下でHTTPS判定を正しくする
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # HTTPS通信でのみCookieを送る
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # ブラウザ側の基本的なセキュリティ強化
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # HTTPSリダイレクトはALB側で行うならFalseでもOK
    # Django側でも強制する場合は.envで1にする
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "0") == "1"