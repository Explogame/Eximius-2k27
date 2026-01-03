from django.shortcuts import render, redirect

from .forms import ContactForm

# Create your views here.

def home(request):

    context = {
        'title' : 'Home-Page Context Works',
        'year' : 2025,
        'members' : ['ahmad', 'muhammad', 'john']
    }

    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


# Contact View - form for receiving messages and e-mails
def contact(request):   

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]

            context = {
                    'form' : form,
                    'success' : True,
                    'name' : name,
                }

            return render(
                request,
                "core/contact.html",
                context,
            )
    else:
        form = ContactForm()
    
    return render(request, 'core/contact.html', {'form' : form})
