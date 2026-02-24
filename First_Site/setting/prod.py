from First_Site.settings import *
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# PRODUCTION SETTINGS - SECURITY HARDENED
# ============================================================================
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# MUST be set via environment variable in production
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY environment variable is not set. "
        "This is required for production deployment. "
        "Set it in your .env file or environment variables."
    )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'
if DEBUG:
    raise ValueError(
        "DEBUG is set to True in production! This is a security risk. "
        "Set DEBUG=False in your environment variables."
    )

# ALLOWED_HOSTS - MUST be configured via environment variable
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    raise ValueError(
        "ALLOWED_HOSTS environment variable must be set for production. "
        "Example: ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com"
    )

# sites framework
SITE_ID = 1

# Database Configuration - Configure based on environment
# Supports PostgreSQL, MySQL, etc. via environment variables
DB_ENGINE = os.getenv('DB_ENGINE', 'django.db.backends.sqlite3')
if DB_ENGINE == 'django.db.backends.postgresql':
    DATABASES = {
        "default": {
            "ENGINE": DB_ENGINE,
            "NAME": os.getenv('DB_NAME', 'django_db'),
            "USER": os.getenv('DB_USER', 'postgres'),
            "PASSWORD": os.getenv('DB_PASSWORD'),
            "HOST": os.getenv('DB_HOST', 'localhost'),
            "PORT": os.getenv('DB_PORT', '5432'),
            "CONN_MAX_AGE": 600,
            "OPTIONS": {
                "sslmode": "require",
            }
        }
    }
elif DB_ENGINE == 'django.db.backends.mysql':
    DATABASES = {
        "default": {
            "ENGINE": DB_ENGINE,
            "NAME": os.getenv('DB_NAME', 'django_db'),
            "USER": os.getenv('DB_USER', 'root'),
            "PASSWORD": os.getenv('DB_PASSWORD'),
            "HOST": os.getenv('DB_HOST', 'localhost'),
            "PORT": os.getenv('DB_PORT', '3306'),
            "CONN_MAX_AGE": 600,
        }
    }
else:
    # SQLite fallback (not recommended for production)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Static & Media Files Configuration
STATIC_ROOT = os.getenv('STATIC_ROOT', BASE_DIR / 'staticfiles')
MEDIA_ROOT = os.getenv('MEDIA_ROOT', BASE_DIR / 'media')

STATICFILES_DIRS = [
    BASE_DIR / "statics",
]

# Static files storage - Use whitenoise or similar for production
# Uncomment if using WhiteNoise
# STORAGES = {
#     "default": "whitenoise.storage.CompressedManifestStaticFilesStorage",
# }

# Email Configuration - Configure for your email backend
EMAIL_BACKEND = os.getenv(
    'EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend'
)
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# Enhanced Security Settings (already in main settings.py, these are overrides for production)
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Additional Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS Configuration
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cache Configuration (recommended for production)
CACHES = {
    'default': {
        'BACKEND': os.getenv(
            'CACHE_BACKEND',
            'django.core.cache.backends.locmem.LocMemCache'
        ),
        'LOCATION': os.getenv('CACHE_LOCATION', 'django-cache'),
    }
}

# Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = int(os.getenv('SESSION_COOKIE_AGE', '1209600'))

# Logging Configuration for Production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'security': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'security.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file', 'security'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}