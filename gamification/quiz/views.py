from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
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

def fill_mask_question(request, question_num=0):
    quiz_data = QuizData.objects.get(quiz__text=request.session['text_id'])
    question_datas = QuestionData.objects.filter(quiz_data=quiz_data)
    question_count = question_datas.count()
    
    if question_num > question_count - 1:
        return redirect('quiz')
    
    question_data = question_datas[question_num]
    sentence = question_data.sentence
    choices = question_data.options_json_to_tuple()
    mask_index = dict(question_data.options[0])['mask_index']
    masked_sentence = sentence.sentence.split()
    masked_sentence[mask_index] = '_____'
    question = Question.objects.get(question_data=question_data)
    
    context = {
            'masked_sentence': ' '.join(masked_sentence),
            'question_num':question_num + 1,
            'question_count': question_count,
            }
    
    if request.method == 'POST':     
        form = FillMaskForm(request.POST, choices=choices, question=question)

        if form.is_valid():
            question_answer = form.save(commit=False)
            question_answer.question = question
            quiz_answer = QuizAnswer.objects.get(id=request.session['quiz_answer_id'])
            question_answer.quiz_answer = quiz_answer
            question_answer.save()
            context['form'] = form
            
            return redirect('fill_mask_question', question_num=question_num+1)
        else:
            messages.error(request, 'Proszę zaznaczyć odpowiedź!')
            context['form'] = form
  
            return render(request, 'quiz/fill_mask_question.html', context)
    else:
        form = FillMaskForm(choices=choices, question=question)
        context['form'] = form

    return render(request, 'quiz/fill_mask_question.html', context)

def start_quiz(request):
    quiz = Quiz.objects.get(text__id=request.session['text_id'])
    quiz_answer = QuizAnswer(quiz=quiz)
    quiz_answer.save()
    request.session['quiz_answer_id'] = quiz_answer.id
    request.session['quiz_id'] = quiz.id
    
    return redirect('fill_mask_question', question_num=0)

    






