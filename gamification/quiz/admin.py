from django.contrib import admin
from .models import *

class TextAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title', )
    
class SentenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'sentence')

class FillMaskDataAdmin(admin.ModelAdmin):
    list_display = ('id','text_title','sentence','mask_index', "mask_str",'option1_str', 'option1_score','option2_str','option2_score','option3_str', 'option3_score')
    
    def text_title(self, obj):
        return obj.sentence.text.title 
class FillMaskAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'ans', 'note')
    
class GuessReplacementDataAdmin(admin.ModelAdmin):
    list_display = ('text_title', 'short_sentence', 'replacing_str','is_replacement')
    
    def short_sentence(self, obj):
        if len(obj.sentence.sentence) > 100:
            return obj.sentence.sentence[:100] + '...'
        
        return obj.sentence.sentence
       
    def text_title(self, obj):
        return obj.sentence.text.title 
        
    
class GuessReplacementAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'ans_correct')

admin.site.register(Sentence, SentenceAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(FillMaskData, FillMaskDataAdmin)
admin.site.register(FillMaskAnswer, FillMaskAnswerAdmin)
admin.site.register(Quiz)
admin.site.register(GuessReplacementData, GuessReplacementDataAdmin)
admin.site.register(GuessReplacementAnswer, GuessReplacementAnswerAdmin)
    

    
    
