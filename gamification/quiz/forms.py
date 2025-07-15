from django import forms
from .models import WordRating

class RatingForm(forms.ModelForm):
    class Meta:
        model = WordRating
        fields = ['value']
        widgets = {
            'value': forms.NumberInput(attrs={
                'type': 'range',
                'min': '1',
                'max': '10',
                'step': '1',
                'id': 'rating-slider',
                'oninput': 'updateLabel(this.value)'
            })
        }
        labels = {'value': "Twoja ocena"}
