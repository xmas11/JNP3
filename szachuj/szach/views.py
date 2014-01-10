from django.utils import timezone
from django.views.generic import TemplateView, FormView, ListView
from forms import SzachForm
from django.core import serializers
from django.http import HttpResponseRedirect
from models import *
import pika
from szachuj.settings import MQ_NAME


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
                   'localhost'))
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