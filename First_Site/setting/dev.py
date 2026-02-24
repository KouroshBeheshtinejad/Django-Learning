from First_Site.settings import *
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# DEVELOPMENT SETTINGS
# ============================================================================
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# In development, using a default key is acceptable, but NEVER in production
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-dev-key-CHANGE-IN-PRODUCTION'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Allow all hosts in development (MUST be restricted in production)
ALLOWED_HOSTS = ['*']

# sites framework
SITE_ID = 1

# Database Configuration - SQLite for development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Static & Media Files Configuration
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / "statics",
]

# Development-specific middleware (Debug toolbar enabled)
if DEBUG:
    if 'debug_toolbar' not in INSTALLED_APPS:
        INSTALLED_APPS.append('debug_toolbar')
    if 'debug_toolbar.middleware.DebugToolbarMiddleware' not in MIDDLEWARE:
        MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# Disable security features in development for ease of development
SECURE_SSL_REDIRECT = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False

# Email configuration for testing (console backend)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging setup for development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}