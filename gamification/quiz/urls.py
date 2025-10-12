from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz, name='quiz' ),
    path('quiz_info', views.quiz_info, name='quiz_info'),
    path('topic_choice', views.topic_choice, name='topic_choice'),  
    path('start_quiz', views.start_quiz, name='start_quiz'),
    path('fill_mask_question/<int:question_num>', views.fill_mask_question, name='fill_mask_question'),
]