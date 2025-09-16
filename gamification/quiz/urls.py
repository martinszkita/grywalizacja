from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz, name='quiz' ),
    path('mask_fill_question', views.fill_mask_question, name='fill_mask_question'),
    
]