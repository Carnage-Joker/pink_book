import os
from pathlib import Path
from django.utils.timezone import get_current_timezone


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"
HUGGING_FACE_API_KEY = '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'
# Template directories
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Ensure templates are pointed here
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
SECRET_KEY = '43299421-902e-4338-8598-98546daef10b'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']

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
    'virtual_try_on',
    'corsheaders',
    # 'csp',  # Disabled for now
    'channels',
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
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  
    "http://www.thepinkbook.com",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
]
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

# settings.py
# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Use 587 for TLS
EMAIL_USE_TLS = True  # Enable TLS
EMAIL_HOST_USER = 'dpinkbook@gmail.com'  # Replace with your Gmail address
# Replace with your Gmail password or app-specific password
EMAIL_HOST_PASSWORD = 'Notthepinkstory1!'
DEFAULT_FROM_EMAIL = 'dpinkbook@gmail.com'


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

# Define a constant for the literal "'self'"
SELF = "'self'"

# Additional settings for CSP if needed (currently disabled)
CSP_DEFAULT_SRC = (SELF,)
CSP_SCRIPT_SRC = (SELF, "https://static.cloudflareinsights.com",
                  "https://perchance.org", "'unsafe-inline'")
CSP_STYLE_SRC = (SELF, "https://fonts.googleapis.com", "'unsafe-inline'")
CSP_FONT_SRC = (SELF, "https://fonts.gstatic.com")

SITE_ID = 1
