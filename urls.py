from django.conf.urls.defaults import *
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from gst.video import VideoFilter

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^Project/', include('Project.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^login/$', 'VideoStoreApp.views.login'),

    (r'^register/$', 'VideoStoreApp.views.register'),

    (r'^upload/$', 'VideoStoreApp.views.videoUpload'),

    (r'^home/$', 'VideoStoreApp.views.HomePage'),

    (r'^logout/$', 'VideoStoreApp.views.Logout'),

    (r'^$', 'VideoStoreApp.views.login'),

    (r'^download/$', 'VideoStoreApp.views.download'),

    (r'^search/$', 'VideoStoreApp.views.search'),



)
baseurlregex = r'^media/(?P<path>.*)$'
baseurlregex_ = r'^static/(?P<path>.*)$'
urlpatterns += patterns('', (baseurlregex, 'django.views.static.serve', {'document_root':  settings.MEDIA_ROOT}),)
urlpatterns += patterns('', (baseurlregex_, 'django.views.static.serve', {'document_root':  settings.STATIC_ROOT}),)
