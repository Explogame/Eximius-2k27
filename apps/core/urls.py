
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'), # Home page
    path('about/', views.about, name='about'), # About page
    path('contact/', views.contact, name='contact'), # Contact page
    path('inbox/', views.inbox, name='inbox'),
    path('mark_as_read/<int:message_id>/', views.mark_as_read, name='mark_as_read'), # Mark message as read
    path('inbox/<int:message_id>/', views.message_detail, name='message_detail'), # Message detail view
    ]

