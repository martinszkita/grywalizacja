from django.forms import ModelForm
from django import forms
from .models import *

class FillMaskForm(ModelForm):
    answer = forms.ChoiceField(widget=forms.RadioSelect)
    
    class Meta:
        model = QuestionAnswer
        fields = ['answer', 'user_comment']
        
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', None)
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        
        if choices:
            self.fields['answer'].choices = choices
        

            
            

    
     
