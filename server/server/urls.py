from django.conf.urls import patterns, include, url
from heatmap.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^location/coord/(?P<latitude>\d+(\.\d+)?)/(?P<longitude>\d+(\.\d+)?)/datetime/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', 'heatmap.views.find_locations'),
    url(r'^location/coord/(?P<latitude>\d+(\.\d+)?)/(?P<longitude>\d+(\.\d+)?)/$', 'heatmap.views.find_all_locations'),
)