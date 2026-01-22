from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ['eximius.onrender.com']  # Replace with your app domain

# Supabase/PostgreSQL
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

# Security
CSRF_TRUSTED_ORIGINS = ['https://your-app.onrender.com']
SECURE_SSL_REDIRECT = True

# Static
STATIC_ROOT = BASE_DIR / 'staticfiles'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

