from django.shortcuts import render, HttpResponse
from quiz.models import *

def home(request):
    return render(request, 'gamification/home.html', {})

    
def stats(request):
    total_answers = QuestionAnswer.objects.all().count()
    total_questions = Question.objects.all().count()
    total_quiz_taken = QuizAnswer.objects.all().count()
    total_users = QuizAnswer.objects.values('username').distinct().count()
    
    stats = {'total_answers': total_answers,
               'total_questions': total_questions,
               'total_quiz_taken': total_quiz_taken,
               'total_users': total_users
               }
    
    print(stats.items())
    
    return render(request, 'gamification/stats.html', {'stats_items':stats.items()})