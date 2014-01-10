from django import forms
from models import Szach


class SzachForm(forms.ModelForm):
    class Meta:
        model = Szach