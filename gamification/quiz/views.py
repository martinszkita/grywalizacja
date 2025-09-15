from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import strip_tags
import random
import re


# Create your views here.
def quiz(request):
    return render(request, 'quiz/quiz.html')






