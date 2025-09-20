from django.shortcuts import render, redirect
from .models import *
from .forms import *
import random

# Create your views here.
def quiz(request):
    return redirect('fill_mask_question')
    # return render(request, 'quiz/quiz.html')

def fill_mask_question(request):
    context = {}
    fill_mask_data = FillMaskData.objects.get(pk=6) # TODO
    sentence_obj = fill_mask_data.sentence
    choices = [(1, fill_mask_data.option1_str), (2, fill_mask_data.option2_str), (3,fill_mask_data.option3_str)]
    
    if request.method == 'POST':
        form = FillMaskQuestionForm(request.POST, choices=choices, sentence=sentence_obj)
        if form.is_valid():
            form.save()
            return redirect('fill_mask_question')
    else:
        form = FillMaskQuestionForm(choices=choices, sentence=sentence_obj)
        mask_index = fill_mask_data.mask_index
        sentence_text = sentence_obj.sentence
        sentence_masked = sentence_text.split()
        sentence_masked[mask_index] = '_____'
        sentence_masked=" ".join(sentence_masked)
        context['sentence'] = sentence_masked
        
    context['form'] = form
        
    return render(request, 'quiz/fill_mask_question.html', context)    
    
    






