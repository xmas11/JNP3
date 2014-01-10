from django.conf.urls import patterns, include, url

from django.contrib import admin
from szach.views import MainPageView, SzachView, SzachSuccessView


admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'szachuj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', MainPageView.as_view(), name='main_view'),
    url(r'^szach/$', SzachView.as_view(), name='szach_view'),
    url(r'^szach_success/$', SzachSuccessView.as_view(), name='szach_success_view'),
    url(r'^admin/', include(admin.site.urls)),
)
