from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz, name='quiz' ),
    path('quiz_info', views.quiz_info, name='quiz_info'),
    path('topic_choice', views.topic_choice, name='topic_choice'),
    path('start_quiz', views.start_quiz, name='start_quiz'),
    path(
        'question/<slug:section>/<int:question_num>',
        views.question,
        name='question'
    ),
    path('feedback', views.feedback, name='feedback'),
    path('quiz_end', views.quiz_end, name='quiz_end'),
]