
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.db.models import Count

from .forms import ContactMessageForm, SignUpForm
from .models import ContactMessage

# Create your views here.

def home(request):
    return render(request, 'core/home.html')


def about(request):
    return render(request, 'core/about.html')

def staff_required(user):
    return user.is_staff

@login_required
@user_passes_test(staff_required)
@permission_required('core.can_view_inbox', raise_exception=True)
def inbox(request):

    messages_list = ContactMessage.objects.filter(is_archived=False).order_by('-created_at')

    paginator = Paginator(messages_list, 5)  # Show 5 messages per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = { 
        'total_messages' : paginator.count,
        'page_obj': page_obj,
        }
    return render(request, 'core/inbox.html', context)

@login_required
@permission_required('core.can_archive_message', raise_exception=True)
def archive_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    message.is_archived = True
    message.save()
    return redirect('core:inbox')

@login_required
@user_passes_test(staff_required)
@permission_required('core.can_mark_as_read', raise_exception=True)
def mark_as_read(request, message_id):
    try:
        message = get_object_or_404(ContactMessage, id=message_id)
        message.is_read = True
        message.save()
    except ContactMessage.DoesNotExist:
        pass
    return redirect('core:inbox')

@login_required
@permission_required('core.can_view_dashboard', raise_exception=True)
def dashboard(request):
    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False, is_archived=False).count()
    archived_messages = ContactMessage.objects.filter(is_archived=True).count()
    today_messages = ContactMessage.objects.filter(created_at__date=now().date()).count()

    context = {
        'total_messages' : total_messages,
        'unread_messsages' : unread_messages,
        'archived_messages' : archived_messages,
        'today_messages' : today_messages,
    }

    return render(request, 'core/dashboard.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('core:home')
    else:
        form = SignUpForm(request.POST)
    return render(request, 'core/signup.html', {'form' : form})

@login_required
@user_passes_test(staff_required)
def message_detail(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)

    if not message.is_read:
        message.is_read = True
        message.save()

    return render(request, 'core/message_detail.html', {'message': message})


# Contact View - form for receiving messages and e-mails
def contact(request):   

    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:contact')
    else:
        form = ContactMessageForm()
    
    return render(request, 'core/contact.html', {'form' : form})
