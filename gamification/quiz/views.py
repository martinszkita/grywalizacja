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
        text = Text.objects.get(title=chosen_topic)
        quiz = Quiz()
        quiz.save()
        quiz.texts.add(text)
        request.session['quiz_id'] = quiz.id
        
        return redirect('fill_mask_question', text_title=chosen_topic, question_num=1)
    
    return render(request, 'quiz/topic_choice.html', {'texts': texts})

def fill_mask_question(request, text_title, question_num=1):
    context = {}
    sentences = Sentence.objects.filter(text__title=text_title, text__question_type=Text.QuestionType.FILL_MASK).order_by('id')
    sentence = sentences[question_num-1]
    question_count = sentences.count()
    fill_mask_data = FillMaskData.objects.get(sentence=sentence)
    quiz_id = request.session['quiz_id']

    choices = [
        (1, fill_mask_data.option1_str),
        (2, fill_mask_data.option2_str),
        (3, fill_mask_data.option3_str)
    ]
    
    if request.method == 'POST':
        form = FillMaskQuestionForm(request.POST, choices=choices, sentence=sentence, quiz_id=quiz_id)
        if form.is_valid():
            form.save()
            if question_num < question_count - 1:
                return redirect('fill_mask_question', text_title=text_title, question_num=question_num + 1)
            else:
                return redirect('guess_replacement_question', text_title=text_title, question_num=1) # nastepny etap quizu
        else:
            print(form.errors.as_text())
            # TODO dac error message ze trzeba wybrac jakas opcje
            return redirect('fill_mask_question', text_title=text_title, question_num=question_num)
    else:
        form = FillMaskQuestionForm(choices=choices, sentence=sentence, quiz_id=quiz_id)
        mask_index = fill_mask_data.mask_index
        sentence_text = sentence.sentence
        sentence_masked = sentence_text.split()
        sentence_masked[mask_index] = '_____'
        sentence_masked = " ".join(sentence_masked)
        context['sentence'] = sentence_masked
        
    context['form'] = form
    context['question_num'] = question_num
    
    return render(request, 'quiz/fill_mask_question.html', context)
   
def guess_replacement_question(request, text_title, question_num=1):
    quiz_id = request.session['quiz_id']
    text = Text.objects.get(title=text_title, question_type=Text.QuestionType.GUESS_REPLACEMENT)
    sentences = Sentence.objects.filter(text=text).order_by('id')
    print(sentences)
    sentence = sentences[question_num-1]
    question_count = sentences.count()
    context = {}
    
    if request.method == 'POST':
        form = GuessReplacementForm(request.POST, sentence=sentence, quiz_id=quiz_id)
        if form.is_valid():
            form.save()
            if question_num < question_count - 1:
                return redirect('guess_replacement_question', text_title=text_title, question_num=question_num + 1)
            else:
                return redirect('summary')
        else:
            print(form.errors.as_text())
            # TODO dac error message ze trzeba wybrac jakas opcje
            return redirect('guess_replacement_question', text_title=text_title, question_num=question_num)
    else: # GET
        form = GuessReplacementForm(sentence=sentence, quiz_id=quiz_id)
        context['sentence'] = sentence.sentence
        
    context['form'] = form
    context['question_num'] = question_num
    
    return render(request, 'quiz/guess_replacement_question.html', context)

def summary(request):
    # do wyswietlenia : wybrany temat, jakie pytanie jaka odpowiedz
    quiz = Quiz.objects.get(pk=request.session['quiz_id'])
    quiz_topic = quiz.text.title
    context = {'quiz_topic':quiz_topic.upper()}
    
    # fill mask summary
    # guess replacement
    
    return render(request, 'quiz/summary.html', context)
    
    






