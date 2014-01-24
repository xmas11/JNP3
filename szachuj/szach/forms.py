from __future__ import unicode_literals
from django import forms
from django.db import models
from django.forms import TextInput, Textarea
from models import Szach
from haystack import connections
from haystack.constants import DEFAULT_ALIAS
from haystack.query import SearchQuerySet, EmptySearchQuerySet
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, PasswordChangeForm
import re

try:
    from django.utils.encoding import smart_text
except ImportError:
    from django.utils.encoding import smart_unicode as smart_text


def model_choices(using=DEFAULT_ALIAS):
    choices = [("%s.%s" % (m._meta.app_label, m._meta.module_name), capfirst(smart_text(m._meta.verbose_name_plural))) for m in connections[using].get_unified_index().get_indexed_models()]
    return sorted(choices, key=lambda x: x[1])


class SzachForm(forms.ModelForm):
    class Meta:
        model = Szach
        fields = {'subject'}
        widgets = {
            'subject': Textarea(attrs={'class': 'form-control',
                                           'placeholder': 'Subject'})
        }


class SzachSearchForm(forms.Form):
    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(attrs={'class': 'form-control',
                                            'type': 'search'}))

    def __init__(self, *args, **kwargs):
        self.searchqueryset = kwargs.pop('searchqueryset', None)
        self.load_all = kwargs.pop('load_all', False)

        if self.searchqueryset is None:
            self.searchqueryset = SearchQuerySet()

        super(SzachSearchForm, self).__init__(*args, **kwargs)

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return EmptySearchQuerySet()

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        if not self.cleaned_data.get('q'):
            return self.no_query_found()

        #sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])
        print 'Searching for {}'.format(self.cleaned_data['q'])
        sqs = self.searchqueryset.filter(text__startswith=self.cleaned_data['q'])
        print 'Found {}'.format(len(sqs))
        if self.load_all:
            sqs = sqs.load_all()

        return sqs

    def get_suggestion(self):
        if not self.is_valid():
            return None

        return self.searchqueryset.spelling_suggestion(self.cleaned_data['q'])


class SzachModelSearchForm(SzachSearchForm):
    def __init__(self, *args, **kwargs):
        super(SzachModelSearchForm, self).__init__(*args, **kwargs)

    def get_models(self):
        """Return an alphabetical list of model classes in the index."""
        search_models = []

        if self.is_valid():
            search_models.append(Szach)
        return search_models

    def search(self):
        sqs = super(SzachModelSearchForm, self).search()
        return sqs.models(*self.get_models())

class BootstrapForm(object):
	def convert_fields(self):
		for field in self:
			if not field.is_hidden:
				classes = field.field.widget.attrs.get('class','').split()
				if not 'form-control' in classes:
					classes.append('form-control')
				field.field.widget.attrs['class'] = ' '.join(classes)
	def as_bootstrap(self):
		"Returns this form rendered as HTML compatile with bootstrap."
		self.convert_fields()
		return self._html_output(
			normal_row = """<div class="form-group">%(label)s%(field)s%(help_text)s</div>""",
			error_row = '<div class="alert alert-danger">%s</div>',
			row_ender = '</div>',
			help_text_html = '<p class="help-block">%s</p>',
			errors_on_separate_row = True)
        
class SzachUserCreationForm(BootstrapForm, UserCreationForm):
	
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

class BootstrapUserCreationForm(BootstrapForm, UserCreationForm):
	pass

class BootstrapAuthenticationForm(BootstrapForm, AuthenticationForm):
	pass
	
class BootstrapPasswordChangeForm(BootstrapForm, PasswordChangeForm):
	pass	

class BootstrapPasswordResetForm(BootstrapForm, PasswordResetForm):
	pass	
