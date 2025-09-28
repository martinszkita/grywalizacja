from django.shortcuts import render, redirect, reverse
from .models import *
from .forms import *


# Create your views here.
def quiz(request):
    return redirect('quiz_info')
    
def quiz_info(request):
    return render(request, 'quiz/quiz_info.html', {})

def topic_choice(request):
    texts = Text.objects.all()
    chosen_topic = request.GET.get('topic')
    
    if chosen_topic:
        quiz = Quiz()
        quiz.save()
        request.session['quiz_id'] = quiz.id
        
        return redirect('fill_mask_question', text_name=chosen_topic, question_num=1)
    
    return render(request, 'quiz/topic_choice.html', {'texts': texts})

def fill_mask_question(request, text_name, question_num=1):
    context = {}
    sentence_q = Sentence.objects.filter(text__title=text_name).order_by('id')[question_num - 1]
    fill_mask_data = FillMaskData.objects.get(sentence=sentence_q)
    quiz_id = request.session['quiz_id']
    print(f'quiz_id:{quiz_id}')
    
    choices = [
        (1, fill_mask_data.option1_str),
        (2, fill_mask_data.option2_str),
        (3, fill_mask_data.option3_str)
    ]
    
    if request.method == 'POST':
        form = FillMaskQuestionForm(request.POST, choices=choices, sentence=sentence_q, quiz_id=quiz_id)
        if form.is_valid():
            form.save()
            # przekierowanie do następnego pytania
            print(f'q_NUM:{question_num}')
            return redirect('fill_mask_question', text_name=text_name, question_num=question_num + 1)
        else:
            print(form.errors)
    else:
        form = FillMaskQuestionForm(choices=choices, sentence=sentence_q, quiz_id=quiz_id)
        mask_index = fill_mask_data.mask_index
        sentence_text = sentence_q.sentence
        sentence_masked = sentence_text.split()
        sentence_masked[mask_index] = '_____'
        print(sentence_masked)
        sentence_masked = " ".join(sentence_masked)
        context['sentence'] = sentence_masked
        
    context['form'] = form
    context['question_num'] = question_num
    
    return render(request, 'quiz/fill_mask_question.html', context)
   
    
    






