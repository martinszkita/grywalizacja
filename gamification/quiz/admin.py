from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

class QuestionDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'sentence']
    readonly_fields = ['id','sentence', 'mask_str','formatted_options']
    exclude = ['options', 'quiz_data']

    def formatted_options(self, obj):
        data = obj.options or []
        if not data:
            return "—"

        html = "<ul style='padding-left:20px;'>"
        for item in data:
            if "mask_index" in item:
                html += f"<li><strong>mask_index:</strong> {item['mask_index']}</li>"
            elif "token" in item:
                html += f"<li>{item['token']} — <span style='color:#fff;'>({item['score']:.4f})</span></li>"
        html += "</ul>"

        return mark_safe(html)

    formatted_options.short_description = "Opcje"
    
    def sentence(self, question_data_object):
        return question_data_object.sentence.sentence
    
    def mask_str(self, question_data_object):
        index = question_data_object.options[0]['mask_index']
        return question_data_object.sentence.sentence.split()[index]

    formatted_options.short_description = "Opcje (token : score)"
    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id','text' ,'question_type', 'sentence',]
    
    def sentence(self, question_object):
        return question_object.question_data.sentence.sentence
    
    def text(self, question_object):
        return question_object.question_data.sentence.text.title
    
class QuizDataAdmin(admin.ModelAdmin):
    list_display = ['text_title', 'question_number']
    readonly_fields = ['text_title', ]
    exclude = ['quiz', ]
    
    def text_title(self, quiz_data_object):
        return quiz_data_object.quiz.text.title
    
    def question_number(self, quiz_data_object):
        return QuestionData.objects.filter(quiz_data=quiz_data_object).count()

class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'user_name', 'text_title']
    readonly_fields = ['id', 'date', 'user_name', 'text_title', 'user_feedback', 'user_comment']
    exclude = ['quiz', ]
    
    def text_title(self, quiz_answer_obj):
        return quiz_answer_obj.quiz.text.title

class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['id','date', 'text_title', 'user_name']   
    
    def text_title(self, question_answer_obj):
        return question_answer_obj.quiz_answer.quiz.text.title
    
    def user_name(self, question_answer_obj):
        return question_answer_obj.quiz_answer.user_name
    
    def date(self, question_answer_obj):
        return question_answer_obj.quiz_answer.date
    
admin.site.register(Text)
admin.site.register(Sentence)
admin.site.register(Question,QuestionAdmin)
admin.site.register(QuestionData, QuestionDataAdmin)
admin.site.register(QuizData, QuizDataAdmin)
admin.site.register(Quiz)
admin.site.register(QuizAnswer, QuizAnswerAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
    
