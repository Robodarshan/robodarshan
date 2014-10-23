from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from accounts import views


urlpatterns = patterns('',
                       url(r'^login/$', views.login, name='login'),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^verify/', views.verify, name='verify'),
                       url(r'^forgot/', views.forgot, name='forgot'),
                       url(r'^reset/', views.reset, name='reset'),
                       url(r'^profile/$', views.profile, name='profile'),
                       url(r'^profile/edit$', views.profile_edit,
                           name='profile_edit'),
                       url(r'^$', RedirectView.as_view(
                           url=reverse_lazy('accounts:profile'))),
                       )
