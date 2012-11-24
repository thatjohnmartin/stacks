from django.conf.urls import patterns, include, url
#from django.core.urlresolvers import reverse
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # homepage
    url(r'^$', 'stacks.www.views.home', name='home'),

    # admin URLs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # authentication
    url(r'^signin/$', 'django.contrib.auth.views.login', {'template_name': 'www/signin.html'}),
    url(r'^signout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^join/$', 'stacks.www.views.join', name='join'),

    # everything URL
    url(r'^(?P<slug>[\w-]+)/$', 'stacks.www.views.thing', name='thing'),
)
