from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'robodarshan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('main.urls', namespace='main')),    
    url(r'^home/', include('main.urls', namespace='main')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^accounts/', include('accounts.urls', namespace= 'accounts')),
    url(r'^stories/', include('blog.urls', namespace= 'blog')),
)
