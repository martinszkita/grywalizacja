from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz, name='quiz' ),
    path('sentence/', views.display_sentence, name='display_sentence'),
    path('rate_word', views.rate_word, name="rate_word"),
    path('rated_words_list', views.rated_words_list, name= 'rated_words_list'),
    
    ]