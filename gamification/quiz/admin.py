from django.contrib import admin
from .models import *

class TextAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title', )
    readonly_fields = ( 'title',)
    
class SentenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'sentence')
    readonly_fields = ('id',)

class FillMaskDataAdmin(admin.ModelAdmin):
    list_display = ('id','sentence','mask_index', "mask_str",'option1_str', 'option1_score','option2_str','option2_score','option3_str', 'option3_score')
    readonly_fields=list_display
    
class FillMaskAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'ans', 'note')
    readonly_fields = list_display
    

admin.site.register(Sentence, SentenceAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(FillMaskData, FillMaskDataAdmin)
admin.site.register(FillMaskAnswer, FillMaskAnswerAdmin)
    

    
    
