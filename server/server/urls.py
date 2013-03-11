from django.conf.urls import patterns, include, url
from heatmap.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('heatmap.views',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^location/coord/(?P<latitude>\d+(\.\d+)?)/(?P<longitude>\d+(\.\d+)?)/datetime/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', 'find_locations_radius_time'),
    url(r'^location/coord/(?P<latitude>\d+(\.\d+)?)/(?P<longitude>\d+(\.\d+)?)/radius/(?P<radius>\d+(\.\d+)?)/$', 'find_locations_radius'),
    url(r'^location/all/$', 'find_locations_all'),
    url(r'^add/coord/(?P<latitude>\d+(\.\d+)?)/(?P<longitude>\d+(\.\d+)?)/$', 'add_location_now'),
)