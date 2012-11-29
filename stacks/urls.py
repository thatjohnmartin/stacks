from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from stacks.www.views.upload import MediaItemCreateView, MediaItemDeleteView

admin.autodiscover()

urlpatterns = patterns('',
    # admin URLs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # authentication
    url(r'^signin/$', 'django.contrib.auth.views.login', {'template_name': 'www/signin.html'}, name="sign_in"),
    url(r'^signout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="sign_out"),

    # served uploaded media
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += patterns('stacks.www.views',
    # homepage
    url(r'^$', 'listing.home', name='home'),

    # external uploader
    url(r'^upload/new/$', MediaItemCreateView.as_view(), name='upload_new'),
    url(r'^upload/delete/(?P<pk>\d+)$', MediaItemDeleteView.as_view(), name='upload_delete'),

    # authentication
    url(r'^join/$', 'join.join', name='join'),

    # uploader + creation
    url(r'^create/$', 'create.create', name='create'),

    # topic home
    url(r'^(?P<topic>astro|auto|ui)/$', 'listing.topic_home', name='topic_home'),

    # user home
    url(r'^(?P<username>[\w-]+)/$', 'listing.user_home', name='user_home'),

    # pages
    url(r'^(?P<topic>astro|auto|ui)/(?P<slug>[\w-]+)/$', 'page.page', name='page'),
)
