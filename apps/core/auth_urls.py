
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup

app_name = 'auth'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Sign Up path
    path('signup/', signup, name='signup'),
]