from django.contrib import admin
from .models import *

admin.site.register(Text)
admin.site.register(Sentence)
admin.site.register(Question)
admin.site.register(QuestionData)
admin.site.register(QuizData)
admin.site.register(Quiz)
    
