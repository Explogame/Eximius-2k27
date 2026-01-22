from django.apps import AppConfig
from django.contrib.auth import get_user_model
import os

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'

    def ready(self):
        User = get_user_model()

        admin_email = os.getenv("ADMIN_EMAIL")
        admin_username = os.getenv("ADMIN_USERNAME")
        admin_password = os.getenv("ADMIN_PASSWORD")

        if admin_email and admin_username and admin_password:
            if not User.objects.filter(username=admin_username).exists():
                User.objects.create_superuser(
                    username=admin_username,
                    email=admin_email,
                    password=admin_password
                )
