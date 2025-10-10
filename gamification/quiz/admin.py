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
    

admin.site.register(Text)
admin.site.register(Sentence)
admin.site.register(Question,QuestionAdmin)
admin.site.register(QuestionData, QuestionDataAdmin)
admin.site.register(QuizData)
admin.site.register(Quiz)
    
