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
        widgets = {
            'signature': TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Signature'}),
            'content': Textarea(attrs={'class': 'form-control',
                                           'placeholder': 'Content'})
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

        sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])

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