from django import forms
from .models import WordRating, InsertWord, ChooseWord

class RatingForm(forms.ModelForm):
    class Meta:
        model = WordRating
        fields = ['value' ]
        widgets = {
            'value': forms.NumberInput( attrs={
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

        
class InsertWordForm(forms.ModelForm):
    class Meta:
        model = InsertWord
        fields = ['inserted_word']
        widgets = {
            'inserted_word' : forms.TextInput()
        }
        labels = {
            'inserted_word':"Twoje słowo:"
        }
    

class ChooseWordForm(forms.ModelForm):
    def __init__(self, choices,*args, **kwargs):
        super(ChooseWordForm, self).__init__(*args, **kwargs)
        self.fields['chosen_word'].choices = choices
        
    
    chosen_word = forms.ChoiceField(widget=forms.RadioSelect)
    class Meta:
        model = ChooseWord
        fields = ['chosen_word']
        labels = {
            'chosen_word':'Wybierz pasujące słowo:'
        }
        
        