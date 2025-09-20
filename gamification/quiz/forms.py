from django import forms
from .models import *


class FillMaskQuestionForm(forms.ModelForm):
    ans = forms.ChoiceField(choices=[], widget=forms.RadioSelect(attrs={'class': 'btn-check'}))

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', None)
        self.sentence_obj = kwargs.pop('sentence', None)
        super().__init__(*args, **kwargs)
        
        if choices:
            self.fields['ans'].choices=choices

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.sentence_obj:
            instance.sentence = self.sentence_obj
        if commit:
            instance.save()
            
    class Meta:
        model = FillMaskAnswer
        fields= ['ans', 'note']
