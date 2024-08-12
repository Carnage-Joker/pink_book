import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"
HUGGING_FACE_API_KEY = os
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
]

# Middleware framework
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'csp.middleware.CSPMiddleware',  # Disabled for now
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Add your frontend URL
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

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication settings
AUTH_USER_MODEL = 'journal.CustomUser'
AUTH_PROFILE = 'journal:UserProfile'
LOGIN_URL = 'journal:welcome'
LOGIN_REDIRECT_URL = 'journal:dashboard'
LOGOUT_REDIRECT_URL = 'journal:login'

# Define a constant for the literal "'self'"
SELF = "'self'"

# Additional settings for CSP if needed (currently disabled)
CSP_DEFAULT_SRC = (SELF,)
CSP_SCRIPT_SRC = (SELF, "https://static.cloudflareinsights.com",
                  "https://perchance.org", "'unsafe-inline'")
CSP_STYLE_SRC = (SELF, "https://fonts.googleapis.com", "'unsafe-inline'")
CSP_FONT_SRC = (SELF, "https://fonts.gstatic.com")

SITE_ID = 1
