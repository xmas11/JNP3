from django.utils import timezone
from django.views.generic import TemplateView, FormView, ListView
from forms import SzachForm, SzachUserCreationForm
from django.core import serializers
from django.http import HttpResponseRedirect
from models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout

from django.template.response import TemplateResponse
from django.contrib import messages

#Authentication
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import django.contrib.auth.views as auth_views
from django.shortcuts import redirect

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
        
def Login(request):
	return auth_views.login(request,
		template_name='accounts/login.html',
		authentication_form=AuthenticationForm)

def Logout(request):
	return auth_views.logout(request, template_name='accounts/logout.html')

def Register(request):
	template_name = 'accounts/register.html'

	if (request.method == 'POST'):
		form = SzachUserCreationForm(request.POST)

		if form.is_valid():
	        # All validation rules pass
            # Process the data in form.cleaned_data

			new_user = form.save()
			messages.success(request, ('Account {name} created.').format(name=new_user.username))

			return redirect('/accounts/login')

	else:
		form = SzachUserCreationForm()

	return TemplateResponse(request, template_name, {'form': form,})

@login_required
def PasswordChange(request):
	return auth_views.password_change(request,
		template_name='accounts/password_change.html',
		password_change_form=PasswordChangeForm,
		post_change_redirect='/accounts/profile')

@login_required
def Profile(request):
	template_name = 'accounts/profile.html'

	return TemplateResponse(request, template_name, {})
