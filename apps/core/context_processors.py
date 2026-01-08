
from .models import ContactMessage

def unread_messages_count(request):

    if request.user.is_authenticated and request.user.is_staff:
        count = ContactMessage.objects.filter(is_read=False).count()
        return {'unread_count': count}
    
    return {}