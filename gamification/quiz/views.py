from django.shortcuts import render, redirect
from .models import *
from .forms import *
import random

# Create your views here.
def quiz(request):
    return render(request, 'quiz/quiz.html')

def fill_mask_question(request):
    context = {}
    random_id = random.randint(0,20)
    o = FillMaskData.objects.get(pk=random_id)
    choices = [(1, o.option1_str), (2, o.option2_str), (3,o.option3_str)]
    
    if request.method == 'POST':
        form = FillMaskQuestionForm(request.POST, choices=choices)
        if form.is_valid():
            form.save()
            return redirect('fill_mask_question')
    else:

        print("view:", choices)
        form = FillMaskQuestionForm(choices=choices)
        sentence = o.sentence.sentence
        mask_index = o.mask_index
        sentence_masked = sentence.split()
        sentence_masked[mask_index] = '_____'
        sentence_masked=" ".join(sentence_masked)
        context['sentence'] = sentence_masked
        
    context['form'] = form
        
    return render(request, 'quiz/fill_mask_question.html', context)    
    
    






