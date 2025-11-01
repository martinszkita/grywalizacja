from django.forms import ModelForm
from django import forms
from .models import *


class FillMaskForm(ModelForm):
    answer = forms.ChoiceField(widget=forms.RadioSelect)
    user_comment = forms.CharField(
        label="Twoja notatka/komentarz do pytania",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Według mnie to pytanie jest bez sensu, bo...",
            }
        ),
        required=False,
    )

    class Meta:
        model = QuestionAnswer
        fields = ["answer", "user_comment"]

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop("choices", None)
        self.question = kwargs.pop("question", None)
        super().__init__(*args, **kwargs)

        if choices:
            self.fields["answer"].choices = choices


class GuessReplacementForm(ModelForm):
    answer = forms.ChoiceField(
        widget=forms.RadioSelect, choices=[("tak", "TAK"), ("nie", "NIE")]
    )
    user_comment = forms.CharField(
        label="Twoja notatka/komentarz do pytania",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Według mnie to pytanie jest bez sensu, bo...",
            }
        ),
        required=False,
    )

    chosen_word = forms.ChoiceField(
        required=False, widget=forms.HiddenInput
    ) 

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop("question", None)
        choices = kwargs.pop('choices', None)
        
        super().__init__(*args, **kwargs)
        
        if choices:
            self.fields['chosen_word'].choices = choices
            
    def cleaned_answer(self):
        is_replaced_answer = self.cleaned_data['answer']
        return {'is_replaced_answer':is_replaced_answer}
        
    def cleaned_chosen_word(self):
        chosen_word_answer = self.cleaned_data['chosen_word']
        return {'chosen_word_answer':chosen_word_answer}
    
    class Meta:
        model = QuestionAnswer
        fields = ["answer", "user_comment", "chosen_word"]
