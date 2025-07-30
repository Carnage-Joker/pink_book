from django.core.management.utils import get_random_secret_key
import os
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# Read secret key from environment or generate one
secret_key = os.getenv('DJANGO_SECRET_KEY') or os.getenv('SECRET_KEY')
if not secret_key:
    secret_key = get_random_secret_key()
SECRET_KEY = secret_key

# Base directory for project
# settings.py
DEFAULT_FIELD_ENCRYPTION_KEY = os.getenv('DEFAULT_FIELD_ENCRYPTION_KEY')  # keep this secret
# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

HUGGING_FACE_API_KEY = os.getenv('HUGGING_FACE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Template directories
TEMPLATES: List[Dict[str, Any]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'templates/dressup'
        ],
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

# Security settings
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,[::1]'
).split(',')

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'fernet_fields',
    'django.contrib.humanize',

    'journal.apps.JournalConfig',
    'dressup',

    'corsheaders',
    'channels',
    'openai',
]

ASGI_APPLICATION = 'Pink_Book.asgi.application'
WSGI_APPLICATION = 'Pink_Book.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'journal.backends.CustomUserModelBackend',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    "http://localhost:3000,http://www.thepinkbook.com.au,"
    "http://localhost:8000,http://127.0.0.1:3000"
).split(',')

ROOT_URLCONF = 'Pink_Book.urls'

# Database
DATABASES: Dict[str, Dict[str, Any]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]

# Email settings
EMAIL_HOST = 'mail.thepinkbook.com.au'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Australia/Sydney'
USE_I18N = True
USE_TZ = True

# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Auth
AUTH_USER_MODEL = 'journal.CustomUser'
LOGIN_URL = 'journal:welcome'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Allauth
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'sissy_name'
ACCOUNT_LOGIN_METHODS = {'username', 'email'}
ACCOUNT_SIGNUP_FIELDS = [
    'email*',
    'username*',
    'password1*',
    'password2*'
]
ACCOUNT_UNIQUE_EMAIL = True

# Cookie timeout
COOKIE_TIMEOUT = 3600

# CSP
SELF = 'self'
CSP_DEFAULT_SRC = (SELF,)
CSP_SCRIPT_SRC = (
    SELF,
    "https://static.cloudflareinsights.com",
    "https://perchance.org",
    "'unsafe-inline'"
)
CSP_STYLE_SRC = (SELF, "https://fonts.googleapis.com", "'unsafe-inline'")
CSP_FONT_SRC = (SELF, "https://fonts.gstatic.com")

# Celery settings (add or update these)

# Use RabbitMQ as broker
CELERY_BROKER_URL = os.getenv(
    'CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672//')

# Use RPC result backend, which rides on the broker but is supported
CELERY_RESULT_BACKEND = 'rpc://'

# (Optional) ignore task results if you don't need them:
CELERY_TASK_IGNORE_RESULT = True

# Don’t run inline now that you have a real broker
CELERY_TASK_ALWAYS_EAGER = False

# Standardize on JSON
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
