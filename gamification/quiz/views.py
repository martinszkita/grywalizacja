from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import strip_tags
from .models import Book, WordRating
from .forms import RatingForm, InsertWordForm
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
    
    book = Book.objects.get(title="Berenice")
    random_sentence = get_random_sentence(book.text)
    rated_word = random.choice(random_sentence.split())

    random_sentence=random_sentence.replace(rated_word, mark_word(rated_word), 1)
    
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.sentence = strip_tags(random_sentence) 
            rating.rated_word = rated_word
            rating.save()
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