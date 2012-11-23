from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # app URLs
    url(r'^$', 'stacks.www.views.home', name='home'),

    # admin URLs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # everything URL
    url(r'^(?P<slug>[\w-]+)/$', 'stacks.www.views.thing', name='thing'),
)
