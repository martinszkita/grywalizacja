from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz, name='quiz' ),
    path('fill_mask_question/<str:text_name>/<int:question_num>/', views.fill_mask_question, name='fill_mask_question'),
    path('quiz_info', views.quiz_info, name='quiz_info'),
    path('topic_choice', views.topic_choice, name='topic_choice'),
    
]