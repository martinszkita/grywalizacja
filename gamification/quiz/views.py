from django.shortcuts import render, redirect
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
        quiz = Quiz(text=Text.objects.get(title=chosen_topic))
        quiz.save()
        request.session['quiz_id'] = quiz.id
        
        return redirect('fill_mask_question', text_name=chosen_topic, question_num=1)
    
    return render(request, 'quiz/topic_choice.html', {'texts': texts})

def fill_mask_question(request, text_name, question_num=1):
    context = {}
    sentence_q = Sentence.objects.filter(text__title=text_name).order_by('id')[question_num - 1]
    fill_mask_data = FillMaskData.objects.get(sentence=sentence_q)
    quiz_id = request.session['quiz_id']
    question_count = Sentence.objects.all().count()

    choices = [
        (1, fill_mask_data.option1_str),
        (2, fill_mask_data.option2_str),
        (3, fill_mask_data.option3_str)
    ]
    
    if request.method == 'POST':
        form = FillMaskQuestionForm(request.POST, choices=choices, sentence=sentence_q, quiz_id=quiz_id)
        if form.is_valid():
            form.save()
            if question_num < question_count - 1:
                return redirect('fill_mask_question', text_name=text_name, question_num=question_num + 1)
            else:
                return redirect('summary')
        else:
            print(form.errors.as_text())
            # TODO dac error message ze trzeba wybrac jakas opcje
            return redirect('fill_mask_question', text_name=text_name, question_num=question_num)
    else:
        form = FillMaskQuestionForm(choices=choices, sentence=sentence_q, quiz_id=quiz_id)
        mask_index = fill_mask_data.mask_index
        sentence_text = sentence_q.sentence
        sentence_masked = sentence_text.split()
        sentence_masked[mask_index] = '_____'
        sentence_masked = " ".join(sentence_masked)
        context['sentence'] = sentence_masked
        
    context['form'] = form
    context['question_num'] = question_num
    
    return render(request, 'quiz/fill_mask_question.html', context)
   
    
def summary(request):
    # do wyswietlenia : wybrany temat, jakie pytanie jaka odpowiedz
    quiz = Quiz.objects.get(pk=request.session['quiz_id'])
    quiz_topic = quiz.text.title
    context = {'quiz_topic':quiz_topic.upper()}
    
    # fill mask summary
    # guess replacement
    
    return render(request, 'quiz/summary.html', context)
    
    






