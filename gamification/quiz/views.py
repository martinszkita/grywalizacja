from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import strip_tags
from .models import Book, WordRating
from .forms import RatingForm, InsertWordForm, ChooseWordForm
import random
import re

# Create your views here.
def quiz(request):
    return render(request, 'quiz/quiz.html')

def get_random_sentence(tekst):
    zdania = re.split(r'(?<=[.!?])\s+', tekst.strip())
    zdania = [z.strip() for z in zdania if z.strip()] 

    if not zdania:
        return "Brak zdań w tekście."

    return random.choice(zdania)

    
def display_sentence(request):
    book = Book.objects.get(title="Berenice")
    random_sentence = get_random_sentence(book.text)
    
    return render(request, 'quiz/sentence.html', {
        'random_sentence': random_sentence})
    
# gra nr1 - ocena dopasowania slowa w zdaniu
def rate_word(request):
    def mark_word(word):
        return (f"<u>{word}</u>")
    
    if request.method == 'GET':
        book = Book.objects.get(title="Berenice")
        random_sentence = get_random_sentence(book.text)
        rated_word = random.choice(random_sentence.split())
        random_sentence=random_sentence.replace(rated_word, mark_word(rated_word), 1)
        
        request.session['random_sentence'] = random_sentence
        request.session['rated_word'] = rated_word
    else:
        random_sentence = request.session.get('random_sentence')
        rated_word = request.session.get('rated_word')
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.sentence = strip_tags(random_sentence) 
            rating.rated_word = rated_word
            rating.save()
            
            del request.session['random_sentence']
            del request.session['rated_word']
            
            return redirect('rate_word')
    else:

        form = RatingForm()
    
    context = {'random_sentence': random_sentence, 'rated_word': rated_word, "form": form}
    
    return render(request, 'quiz/rate_word.html', context)

def insert_word(request):
    book = Book.objects.get(id=1)
    random_sentence = get_random_sentence(book.text)
    hidden_word = random.choice(random_sentence.split())
    
    if request.method == 'POST':
        form = InsertWordForm(request.POST)
        if form.is_valid():
            full_form = form.save(commit=False)
            full_form.sentence = random_sentence
            full_form.hidden_word = hidden_word
            full_form.save()
    
            return redirect('insert_word')
    else:
        form = InsertWordForm()
        
    return render(request, 'quiz/insert_word.html', {'form': form,'random_sentence':random_sentence, 'hidden_word':hidden_word})  

def rated_words_list(request):
    rated_words = WordRating.objects.all()
    table_columns = [field.name for field in WordRating._meta.fields]
    print(table_columns)
    return render(request, 'quiz/rated_words_list.html', {'rated_words' : rated_words, 'table_columns':table_columns})

def choose_word(request):
    if request.method == 'GET':
        book = Book.objects.get(id=1)
        random_sentence = get_random_sentence(book.text)
        hidden_word = random.choice(random_sentence.split())

        choices = []
        while len(choices) < 3:
            word = random.choice(random_sentence.split())
            if word != hidden_word and [word, word] not in choices:
                choices.append([word, word])  # jako lista

        choices.append([hidden_word, hidden_word])
        random.shuffle(choices)

        request.session['random_sentence'] = random_sentence
        request.session['hidden_word'] = hidden_word
        request.session['choices'] = choices

    else:
        raw_choices = request.session.get('choices')
        if raw_choices is None:
            return redirect('choose_word')  # sesja wygasła lub niepoprawny dostęp

        choices = [tuple(choice) for choice in raw_choices]
        random_sentence = request.session.get('random_sentence')
        hidden_word = request.session.get('hidden_word')

    if request.method == 'POST':
        form = ChooseWordForm(choices, request.POST)
        if form.is_valid():
            full_form = form.save(commit=False)
            full_form.sentence = random_sentence
            full_form.hidden_word = hidden_word
            full_form.option1 = choices[0]
            full_form.save()

            for key in ['random_sentence', 'hidden_word', 'choices']:
                if key in request.session:
                    del request.session[key]

            return redirect('choose_word')
    else:
        form = ChooseWordForm(choices)

    context = {
        'form': form,
        'random_sentence': random_sentence,
        'hidden_word': hidden_word,
    }

    return render(request, 'quiz/choose_word.html', context)
