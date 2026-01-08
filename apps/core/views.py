from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import ContactMessageForm, SignUpForm
from .models import ContactMessage

# Create your views here.

def home(request):
    return render(request, 'core/home.html')


def about(request):
    return render(request, 'core/about.html')

@login_required
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

def mark_as_read(request, message_id):
    try:
        message = ContactMessage.objects.get(id=message_id)
        message.is_read = True
        message.save()
    except ContactMessage.DoesNotExist:
        pass
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
