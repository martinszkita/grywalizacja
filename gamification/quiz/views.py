from django.shortcuts import render
from .models import Book


# Create your views here.
def display_random_sentence(request):
    book = Book.objects.all()
    random_sentence = book.get_random_sentence() if book else "No book available"

    return render(request, 'quiz/random_sentence.html', {
        'random_sentence': random_sentence})