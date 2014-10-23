from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from main import views

urlpatterns = patterns('',
                       url(r'^$', views.home, name='home'),
                       )
