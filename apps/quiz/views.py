from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators  import login_required
from .models import Quiz, Question
from .forms import QuizForm, QuestionForm, ChoiceForm

# Create your views here.

# Quiz Creation View
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.creator = request.user
            quiz.save()
            return redirect('add_question', quiz_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, 'quiz/create_quiz.html', {'form': form})


# Question Addng View
@login_required
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, creator=request.user)
    if request.method == 'POST':
        q_form = QuestionForm(request.POST)
        if q_form.is_valid:
            question = q_form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('add_choice', question_id=question.id)
    else:
        q_form = QuestionForm()

    context = {
        'quiz' : quiz,
        'form' : q_form,
    }

    return render(request, 'quiz/add_question.html', context)


# Choice Adding View
@login_required
def add_choice(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        c_form = ChoiceForm(request.POST)
        if c_form.is_valid():
            choice = c_form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('add_choice', question_id=question.id)
    else:
        c_form = ChoiceForm()

    context = {
        'question' : question,
        'form' : c_form,
    }
    
    return render(request, 'quiz/add_choice.html', context)


