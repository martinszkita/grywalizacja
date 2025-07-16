from django import forms
from .models import WordRating

class RatingForm(forms.ModelForm):
    class Meta:
        model = WordRating
        fields = ['value', 'rated_word']
        widgets = {
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'range',
                'min': '1',
                'max': '10',
                'step': '1',
                'id': 'rating-slider',
                'oninput': 'updateLabel(this.value)'
            })
        }
        labels = {'value': "Twoja ocena w skali od 0-10"}
