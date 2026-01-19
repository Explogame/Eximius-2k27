from django.db import models

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
