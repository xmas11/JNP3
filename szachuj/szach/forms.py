from django import forms
import re
from django.forms import TextInput, Textarea
from models import Szach
from django.contrib.auth.forms import UserCreationForm

class SzachForm(forms.ModelForm):
    class Meta:
        model = Szach
        widgets = {
            'signature': TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Signature'}),
            'content': Textarea(attrs={'class': 'form-control',
                                           'placeholder': 'Content'})
        }

class SzachUserCreationForm(UserCreationForm):
	
	password_regex = [re.compile(regex) for regex in [r'\W', r'[A-Z]', r'\d']]
	password_min_length = 6
	
	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code='password_mismatch',
			)
			
		for regex in self.password_regex:
			if not regex.search(password1):
				raise forms.ValidationError(
					"Password must contain a decimal, capital character and non-alphanumeric character",
					code='password_mismatch',
				)
				
		if len(password1) < self.password_min_length:
			raise forms.ValidationError(
				"Password must be at least {length} characters long.".format(length = self.password_min_length),
				code='password_mismatch',
			)
			
		return password2
