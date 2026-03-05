from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<int:message_id>/', views.message_detail, name='message_detail'),
    path('mark_as_read/<int:message_id>/', views.mark_as_read, name='mark_as_read'),
    path('archive/<int:message_id>/', views.archive_message, name='archive_message'),
    path('dashboard/', views.dashboard, name='dashboard'),  # FIX: added trailing slash
]