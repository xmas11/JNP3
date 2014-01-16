from __future__ import unicode_literals
from django.utils import timezone
from django.views.generic import TemplateView, FormView, ListView
from forms import SzachForm, SzachModelSearchForm
from django.core import serializers
from models import *
from haystack.query import EmptySearchQuerySet
import pika
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from szachuj.settings import MQ_NAME

from django.http import Http404


class MainPageView(TemplateView):
    template_name = "index.html"


class SzachView(FormView):
    template_name = "szach.html"
    form_class = SzachForm
    success_url = '/szach_success/'

    def form_valid(self, form):
        content = form.cleaned_data['content']
        signature = form.cleaned_data['signature']
        szach = Szach.objects.create(content=content, signature=signature)
        # Sending data using rabbitMQ

        data_szach = serializers.serialize('xml', [szach])

        # TODO Connection should with runserver, not each time while sending form
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            str('localhost')))
        database_channel = connection.channel()
        database_channel.queue_declare(queue=MQ_NAME)
        database_channel.basic_publish(exchange='',
                                       routing_key=MQ_NAME,
                                       body=data_szach)
        print 'Sending ' + data_szach
        connection.close()
        return super(SzachView, self).form_valid(form)


class SzachSuccessView(TemplateView):
    template_name = "szach_success.html"


class SzachListView(ListView):
    model = Szach
    template_name = "szach_list.html"

    def get_context_data(self, **kwargs):
        context = super(SzachListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


RESULTS_PER_PAGE = 20


class SzachSearchView(object):
    template = 'search/search.html'
    extra_context = {}
    query = ''
    results = EmptySearchQuerySet()
    request = None
    form = None
    results_per_page = RESULTS_PER_PAGE

    def __init__(self, template=None, load_all=True, form_class=None,
                 searchqueryset=None, context_class=RequestContext, results_per_page=None):
        self.load_all = load_all
        self.form_class = form_class
        self.context_class = context_class
        self.searchqueryset = searchqueryset

        if form_class is None:
            self.form_class = SzachModelSearchForm

        if not results_per_page is None:
            self.results_per_page = results_per_page

        if template:
            self.template = template

    def __call__(self, request):
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """
        self.request = request

        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()

        return self.create_response()

    def build_form(self, form_kwargs=None):
        """
        Instantiates the form the class should use to process the search query.
        """
        data = None
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)

        if len(self.request.GET):
            data = self.request.GET

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        return self.form_class(data, **kwargs)

    def get_query(self):
        """
        Returns the query provided by the user.

        Returns an empty string if the query is invalid.
        """
        if self.form.is_valid():
            return self.form.cleaned_data['q']

        return ''

    def get_results(self):
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """
        return self.form.search()

    def build_page(self):
        """
        Paginates the results appropriately.

        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        start_offset = (page_no - 1) * self.results_per_page
        self.results[start_offset:start_offset + self.results_per_page]

        paginator = Paginator(self.results, self.results_per_page)

        try:
            page = paginator.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")

        return (paginator, page)

    def extra_context(self):
        """
        Allows the addition of more context variables as needed.

        Must return a dictionary.
        """
        return {}

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        (paginator, page) = self.build_page()

        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }

        if self.results and hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()

        context.update(self.extra_context())
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))

