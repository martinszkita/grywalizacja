from django.shortcuts import render, redirect
from .models import *
from .forms import *
import random

# Create your views here.
def quiz(request):
    return redirect('quiz_info')
    
def quiz_info(request):
    return render(request, 'quiz/quiz_info.html', {})

def topic_choice(request):
    texts = Text.objects.all()
    return render(request, 'quiz/topic_choice.html', {'texts': texts})

def fill_mask_question(request, text_name, question_num=1):
    context = {}
    sentence_q = Sentence.objects.filter(text__title=text_name).order_by('id')[question_num - 1]
    fill_mask_data = FillMaskData.objects.get(sentence=sentence_q)
    choices = [
        (1, fill_mask_data.option1_str),
        (2, fill_mask_data.option2_str),
        (3, fill_mask_data.option3_str)
    ]
    
    if request.method == 'POST':
        form = FillMaskQuestionForm(request.POST, choices=choices, sentence=sentence_q)
        if form.is_valid():
            form.save()
            # przekierowanie do następnego pytania
            return redirect('fill_mask_question', text_name=text_name, question_num=question_num + 1)
    else:
        form = FillMaskQuestionForm(choices=choices, sentence=sentence_q)
        mask_index = fill_mask_data.mask_index
        sentence_text = sentence_q.sentence
        sentence_masked = sentence_text.split()
        sentence_masked[mask_index] = '_____'
        sentence_masked = " ".join(sentence_masked)
        context['sentence'] = sentence_masked
        
    context['form'] = form
    context['question_num'] = question_num
    
    return render(request, 'quiz/fill_mask_question.html', context)
   
    
    






