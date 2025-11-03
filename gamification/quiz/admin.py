from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

class QuestionDataAdmin(admin.ModelAdmin):
    list_display = ['id','question_type', 'sentence']
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

    formatted_options.short_description = "Opcje" #type: ignore
    
    def question_type(self, question_data_object):
        type_int = Question.objects.get(question_data=question_data_object).question_type

        return Question.QuestionType.labels[type_int]
    
    def sentence(self, question_data_object):
        return question_data_object.sentence.sentence
    
    def mask_str(self, question_data_object):
        index = question_data_object.options[0]['mask_index']
        return question_data_object.sentence.sentence.split()[index]

    formatted_options.short_description = "Opcje (token : score)" #type: ignore
    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id','text' ,'question_type', 'sentence',]
    list_filter = [ 'question_type', ]
    readonly_fields = ['id', 'text', 'question_type', 'sentence']
    
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
    list_display = ['id', 'date',  'text_title', 'answered_questions_num'] # dodac username
    readonly_fields = ['id', 'date',  'text_title', 'answered_questions_num', 'user_feedback', 'user_comment']
    exclude = ['quiz', ]
    
    def text_title(self, quiz_answer_obj):
        return quiz_answer_obj.quiz.text.title

class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['id','date', 'text_title', 'username']   
    
    def text_title(self, question_answer_obj):
        return question_answer_obj.quiz_answer.quiz.text.title
    
    def username(self, question_answer_obj):
        return question_answer_obj.quiz_answer.username
    
    def date(self, question_answer_obj):
        return question_answer_obj.quiz_answer.date

class SentenceAdmin(admin.ModelAdmin):
    list_display = ['id','has_data','text', 'sentence', ]
    readonly_fields = ['sentence','has_data', 'text', ]
    list_filter = ['has_data', 'text']
    
    
admin.site.register(Text)
admin.site.register(Sentence, SentenceAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(QuestionData, QuestionDataAdmin)
admin.site.register(QuizData, QuizDataAdmin)
admin.site.register(Quiz)
admin.site.register(QuizAnswer, QuizAnswerAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
    
