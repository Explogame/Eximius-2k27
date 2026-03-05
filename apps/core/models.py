from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True, default=None)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("can_view_inbox", "Can view inbox"),
            ('can_mark_as_read', "Can mark messages as read"),
            ('can_archive_message', "Can archive messages"),
            ('can_view_dashboard', 'can view dashboard'),
        ]

    def __str__(self):
        return f"Message from {self.name} - {'Read' if self.is_read else 'Unread'}"
    
class Announcement(models.Model):
    PRIORITY_CHOICES = [
        ('info',   'Info'),
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
    ]

    title      = models.CharField(max_length=200)
    body       = models.TextField()
    priority   = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    expires_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcements')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def is_active(self):
        from django.utils.timezone import now
        return self.expires_at is None or self.expires_at > now()
