from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators  import login_required
from .models import Quiz, Question, Attempt, Choice, Answer
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
            return redirect('quiz:add_question', quiz_id=quiz.id)
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
            return redirect('quiz:add_choice', question_id=question.id)
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
            return redirect('quiz:add_choice', question_id=question.id)
    else:
        c_form = ChoiceForm()

    context = {
        'question' : question,
        'quiz': question.quiz,
        'form' : c_form,
    }
    
    return render(request, 'quiz/add_choice.html', context)


# Quiz List View To Show Available Quizzes
def quiz_list(request):
    quizzes = Quiz.objects.order_by('-created_at')
    return render(request, 'quiz/quiz_list.html', {'quizzes' : quizzes})


# Taking Quiz View
@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        score = 0
        attempt = Attempt.objects.create(user=request.user, quiz=quiz)

        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected:
                choice = Choice.objects.get(id=selected)
                correct = choice.is_correct
                if correct:
                    score += 1
                else:
                    score -= quiz.negative_mark

                Answer.objects.create(attempt=attempt,question=question,selected_choice=choice,is_correct=correct)
            else:
                Answer.objects.create(attempt=attempt,question=question,selected_choice=None,is_correct=False)

        attempt.score = score
        attempt.save()
        return redirect('quiz:quiz_result', attempt_id=attempt.id)

    context = {
        'quiz':quiz,
        'questions':questions,
    }

    return render(request, 'quiz/take_quiz.html', context)


# Result View
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(Attempt, id=attempt_id, user=request.user)
    return render(request, 'quiz/quiz_result.html', {'attempt':attempt})
    
                
# User Quiz History
@login_required
def my_attempts(request):
    attempts = Attempt.objects.filter(user=request.user).order_by('-completed_at')
    return render(request, 'quiz/my_attempts.html', {'attempts':attempts})


# Quiz Detail Page View
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions_count = quiz.questions.count()
    attempts = Attempt.objects.filter(quiz=quiz).count()
    attempted = Attempt.objects.filter(user=request.user, quiz=quiz)

    context = {
        'quiz':quiz,
        'questions_count': questions_count,
        'attempts': attempts,
        'attempted': attempted,
    }

    return render(request, 'quiz/quiz_detail.html', context)

