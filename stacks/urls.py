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
    # homepage
    url(r'^$', 'listing.home', name='home'),

    # new uploader
    url(r'^upload/$', 'upload.upload_image', name='upload_image'),

    # authentication
    url(r'^join/$', 'join.join', name='join'),

    # user home
    url(r'^users/(?P<username>[\w-]+)/$', 'listing.user_home', name='user_home'),

    # tags home - tag directory
    url(r'^tags/$', 'listing.tag_home', name='tag_home'),

    # single tag listing page
    url(r'^tags/(?P<tag>[\w-]+)/$', 'listing.tag_list', name='tag_list'),

    # browse pages
    url(r'^stacks/(?P<slug>[\w-]+)/$', 'stack.stack', name='stack'),

    # create and edit page
    url(r'^create/$', 'page.create', name='page.create'),
    url(r'^ajax/edit-stack/$', 'page.edit', name='page.edit'),

    # test page
    url(r'^test/$', 'listing.test')
)
