from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # admin URLs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # authentication
    url(r'^signin/$', 'django.contrib.auth.views.login', {'template_name': 'www/signin.html'}),
    url(r'^signout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)

urlpatterns += patterns('stacks.www.views',
    # homepage
    url(r'^$', 'home', name='home'),

    # authentication
    url(r'^join/$', 'join', name='join'),

    # uploader
    url(r'^upload/$', 'upload', name='upload'),

    # topic home
    url(r'^(?P<topic>astro|auto|ui)/$', 'topic_home', name='topic_home'),

    # user home
    url(r'^(?P<username>[\w-]+)/$', 'user_home', name='user_home'),

    # everything URL
    url(r'^(?P<slug>[\w-]+)/$', 'thing', name='thing'),
)
