

from .base import *
# import dj_database_url

ALLOWED_HOSTS = [
    "eximiusdomain.com"
    "www.eximiusdomain.com"
    "eximius-2k27.onrender.com"
]

'''
DATABASES = {
    "default" : dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_required=True,
    )
}
'''

STATIC_ROOT = BASE_DIR/"staticfiles"
STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

