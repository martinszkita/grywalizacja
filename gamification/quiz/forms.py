from django import forms
from .models import *


class FillMaskQuestionForm(forms.ModelForm):
    ans = forms.ChoiceField(choices=[], widget=forms.RadioSelect)
    
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', None)
        super().__init__(*args, **kwargs)
        print(choices)
        if choices:
            self.fields['ans'].choices=choices
            

    class Meta:
        model = FillMaskAnswer
        fields= ['ans', 'note']

        
    
        