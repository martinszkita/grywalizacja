from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz, name='quiz' ),
    path('sentence/', views.display_sentence, name='display_sentence'),
    
    ]