from django.shortcuts import render, redirect
from .models import Book

# Create your views here.
def quiz(request):
    return render(request, 'quiz/quiz.html')

def get_random_sentence(tekst):
    import random
    import re

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
        
    import random
    book = Book.objects.get(title="Berenice")
    random_sentence = get_random_sentence(book.text)
    random_word = random.choice(random_sentence.split())


    random_sentence=random_sentence.replace(random_word, mark_word(random_word), 1)

    
    context = {'random_sentence': random_sentence, 'random_word': random_word}
    
    return render(request, 'quiz/rate_word.html', context)