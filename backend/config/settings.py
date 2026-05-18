import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 基本設定
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

# settings.py
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEBUG = os.getenv("DEBUG", "1") == "1"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# アプリ
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',

    # 自作
    "apps.users",
    "apps.foods",
    # "apps.shopping_memos",
]

# ミドルウェア
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = 'config.urls'

# テンプレート
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': False,
        'OPTIONS': {
            'environment': 'config.jinja2.environment',
        },
    },
    {
        # Django管理画面は従来のDjangoテンプレートを使うため残す
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'config.wsgi.application'


# データベース(MySQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'db'),   # docker-compose.ymlのサービス名
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}

AUTH_USER_MODEL = 'users.User'

# パスワード
AUTH_PASSWORD_VALIDATORS = []

# 言語・時間
LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True
USE_TZ = False


# Static / Media
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

#GeminiAPI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")