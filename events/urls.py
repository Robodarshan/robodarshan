from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from events import views


urlpatterns = patterns('',
                       url(r'^new/$', views.new, name='new'),
                       url(r'^show/$', views.show, name='show'),
                       url(r'^edit/$', views.edit, name='edit'),
                       )
