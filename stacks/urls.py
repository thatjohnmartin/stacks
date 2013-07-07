from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

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
    # stacks homepage
    url(r'^$', 'listing.stacks_home', name='stacks_home'),

    # authentication
    url(r'^join/$', 'join.join', name='join'),

    # test page
    url(r'^test/$', 'listing.test'),

    # site homepage
    url(r'^(?P<site>[\w-]+)/$', 'listing.site_home', name='site_home'),

    # new uploader
    url(r'^(?P<site>[\w-]+)/upload/$', 'upload.upload_image', name='upload_image'),

    # user home
    url(r'^(?P<site>[\w-]+)/users/(?P<username>[\w-]+)/$', 'listing.user_home', name='user_home'),

    # tags home - tag directory
    url(r'^(?P<site>[\w-]+)/tags/$', 'listing.tag_home', name='tag_home'),

    # single tag listing page
    url(r'^(?P<site>[\w-]+)/tags/(?P<tag>[\w-]+)/$', 'listing.tag_list', name='tag_list'),

    # browse pages
    url(r'^(?P<site>[\w-]+)/stacks/(?P<slug>[\w-]+)/$', 'stack.stack', name='stack'),
)
