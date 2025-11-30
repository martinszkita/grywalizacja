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

    chosen_word = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop("question", None)
        choices = kwargs.pop("choices", None)

        super().__init__(*args, **kwargs)

        if choices:
            self.fields["chosen_word"].choices = choices

    class Meta:
        model = QuestionAnswer
        fields = ["answer", "user_comment", "chosen_word"]


class WsdQuestionForm(ModelForm):
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


class UsernameForm(forms.Form):
    username = forms.CharField(
        label="Jak chcesz zostać zapisany/zapisana w bazie?",
        max_length=20,
        widget=forms.TextInput(
            attrs={"placeholder": "Pszczółka Maja 16", "class": "form-control"}
        ),
        required=True,
    )


class UserFeedbackForm(forms.Form):
    user_feedback = forms.IntegerField(
        label="Jak oceniasz quiz?",
        min_value=0,
        max_value=5,
        required=False,
        widget=forms.HiddenInput(attrs={"id": "id_user_feedback"}),
    )

    user_comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Uwielbiam robić takie quizy..",
                "rows": 3,
                "class": "form-control",
            }
        ),
        required=False,
        label='Co sądzisz o wypełnionym quizie?'
    )
