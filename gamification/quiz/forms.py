from django import forms
from .models import *


class FillMaskQuestionForm(forms.ModelForm):
    ans = forms.ChoiceField(choices=[], widget=forms.RadioSelect(attrs={'class': 'btn-check'}))
    quiz_id = forms.IntegerField(disabled=True)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', None)
        self.quiz_id = kwargs.pop('quiz_id', None)
        self.sentence_obj = kwargs.pop('sentence', None)
        
        super().__init__(*args, **kwargs)
        
        if choices:
            self.fields['ans'].choices=choices  
        
        self.fields['quiz_id'].initial = self.quiz_id
        
    def clean_quiz_id(self):
        return self.quiz_id
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.quiz_id:
            instance.quiz = Quiz.objects.get(id=self.quiz_id)
        if self.sentence_obj:
            instance.sentence = self.sentence_obj
        if commit:
            instance.save()
            
    class Meta:
        model = FillMaskAnswer
        fields= ['ans', 'note', 'quiz_id']
