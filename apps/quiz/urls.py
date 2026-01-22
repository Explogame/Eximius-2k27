
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_quiz, name='create_quiz'),
    path('<int:quiz_id>/add_question/', views.add_question, name='add_question'),
    path('<int:question_id>/add_choice/', views.add_choice, name='add_choice'),
]
