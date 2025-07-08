from django.shortcuts import render, redirect
from .models import Book


# Create your views here.
def quiz(request):
    return redirect(display_sentence)

def display_sentence(request):


    def get_random_sentence(tekst):
        import random
        import re
        # Dzieli tekst na zdania na podstawie kropki, znaku zapytania i wykrzyknika
        zdania = re.split(r'(?<=[.!?])\s+', tekst.strip())
        zdania = [z.strip() for z in zdania if z.strip()]  # Usuwa puste

        if not zdania:
            return "Brak zdań w tekście."

        return random.choice(zdania)
        
    book = Book.objects.get(title="Berenice")

    random_sentence = get_random_sentence(book.text)
    

    return render(request, 'quiz/sentence.html', {
        'random_sentence': random_sentence})
