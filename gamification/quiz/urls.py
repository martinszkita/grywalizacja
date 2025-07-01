from django.urls import path
from . import views

urlpatterns = [
    path('random-sentence/', views.display_random_sentence, name='display_random_sentence'),
    
    ]