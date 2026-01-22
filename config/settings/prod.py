from .base import *
import dj_database_url
import os

DEBUG = False
ALLOWED_HOSTS = ['.onrender.com']

DATABASES = {
    'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Dashboard cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'eximius-cache',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
