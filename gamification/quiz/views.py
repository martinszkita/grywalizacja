from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .forms import *


# Create your views here.
def quiz(request):
    return redirect('quiz_info')
    
def quiz_info(request):
    return render(request, 'quiz/quiz_info.html', {})

def topic_choice(request):
    texts = Text.objects.all()

    chosen_topic  = request.GET.get('topic')
    
    if chosen_topic:
        text = Text.objects.get(title=chosen_topic)
        text_id = text.id
        request.session['text_id'] = text_id
        return redirect('start_quiz')

    return render(request, 'quiz/topic_choice.html', {'texts': texts})


def start_quiz(request):
    return HttpResponse(request)
    






