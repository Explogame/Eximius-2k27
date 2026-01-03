from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ContactMessageForm
from .models import ContactMessage

# Create your views here.

def home(request):
    return render(request, 'core/home.html')


def about(request):
    return render(request, 'core/about.html')

@login_required
def inbox(request):

    messages = ContactMessage.objects.order_by('created_at')
    
    context = {'messages' : messages}
    return render(request, 'core/inbox.html', context)

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
