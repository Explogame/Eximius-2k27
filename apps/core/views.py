
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.core.paginator import Paginator

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

    messages_list = ContactMessage.objects.order_by('-created_at')

    paginator = Paginator(messages_list, 5)  # Show 5 messages per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = { 
        'total_messages' : paginator.count,
        'page_obj': page_obj,
        }
    return render(request, 'core/inbox.html', context)

@login_required
@user_passes_test(staff_required)
@permission_required('core.can_mark_as_read', raise_exception=True)
def mark_as_read(request, message_id):
    try:
        message = ContactMessage.objects.get_object_or_404(id=message_id)
        message.is_read = True
        message.save()
    except ContactMessage.DoesNotExist:
        pass
    return redirect('core:inbox')

@login_required
@user_passes_test(staff_required)
@permission_required('core.can_delete_messages', raise_exception=True)
def delete_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    message.delete()
    return redirect('core:inbox')

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
