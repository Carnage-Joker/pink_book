import os
from pathlib import Path
from django.utils.timezone import get_current_timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"
HUGGING_FACE_API_KEY = os.getenv('HUGGING_FACE_API_KEY')

# Template directories
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Ensure templates are pointed here
        'DIRS': [BASE_DIR / 'templates', 'dressup/templates/dressup'],
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
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS', 'localhost,127.0.0.1,[::1]').split(',')

# Application references
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'journal.apps.JournalConfig',
    'dressup',
    'corsheaders',
    'channels',
    'openai',
    'gmailapi_backend',
]

ASGI_APPLICATION = 'Pink_Book.asgi.application'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Middleware framework
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS', "http://localhost:3000,http://www.thepinkbook.com.au,http://localhost:8000,http://127.0.0.1:3000").split(',')

ROOT_URLCONF = 'Pink_Book.urls'
WSGI_APPLICATION = 'Pink_Book.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Email settings
GMAIL_CLIENT_SECRET_FILE = BASE_DIR / 'client_secret.json'
GMAIL_TOKEN_FILE = BASE_DIR / 'token.json'
EMAIL_BACKEND = 'gmailapi_backend.mail.GmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = get_current_timezone()
USE_I18N = True
USE_TZ = True
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication settings
AUTH_USER_MODEL = 'journal.CustomUser'
LOGIN_URL = 'journal:welcome'
LOGOUT_REDIRECT_URL = 'journal:welcome'

# CSP Settings (currently disabled)
SELF = "'self'"
CSP_DEFAULT_SRC = (SELF,)
CSP_SCRIPT_SRC = (SELF, "https://static.cloudflareinsights.com",
                  "https://perchance.org", "'unsafe-inline'")
CSP_STYLE_SRC = (SELF, "https://fonts.googleapis.com", "'unsafe-inline'")
CSP_FONT_SRC = (SELF, "https://fonts.gstatic.com")

SITE_ID = 1
