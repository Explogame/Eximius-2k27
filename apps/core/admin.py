from django.contrib import admin
from .models import ContactMessage, Announcement

admin.site.register(ContactMessage)
admin.site.register(Announcement)