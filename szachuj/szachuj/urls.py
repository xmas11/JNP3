from django.conf.urls import patterns, include, url

from django.contrib import admin
from views import MainPageView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'szachuj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', MainPageView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
