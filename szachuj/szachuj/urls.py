from django.conf.urls import patterns, include, url

from django.contrib import admin
from szach.views import MainPageView, SzachView, SzachSuccessView, SzachListView
import szach.views as szach_views

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'szachuj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', MainPageView.as_view(), name='main_view'),
    #~ url(r'^logged/$', MainLoggedPageView.as_view(), name='main_logged_view'),
    url(r'^szach/$', SzachView.as_view(), name='szach_view'),
    url(r'^szach_success/$', SzachSuccessView.as_view(), name='szach_success_view'),
    url(r'^szach_list/$', SzachListView.as_view(), name='szach_list_view'),
    url(r'^accounts/login', szach_views.Login, name='szach_login_view'),
    url(r'^accounts/register', szach_views.Register, name='register_view'),
    url(r'^accounts/logout', szach_views.Logout, name='logout_view'),
    url(r'^accounts/password_change', szach_views.PasswordChange, name='passwor_change_view'),
    url(r'^accounts/profile', szach_views.Profile, name='profile_view'),
    #~ url(r'^szach_private/$', SzachPrivateView.as_view(), name='szach_private_view'),
    url(r'^admin/', include(admin.site.urls)),
)
