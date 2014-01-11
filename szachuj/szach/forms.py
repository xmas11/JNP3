from django import forms
from django.forms import TextInput, Textarea
from models import Szach


class SzachForm(forms.ModelForm):
    class Meta:
        model = Szach
        widgets = {
            'signature': TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Signature'}),
            'content': Textarea(attrs={'class': 'form-control',
                                           'placeholder': 'Content'})
        }
