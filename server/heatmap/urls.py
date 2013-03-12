from django.conf.urls import patterns, include, url


timestamp_urlpatterns = patterns('heatmap.views',	
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'search'),
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/$', 'search'),
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', 'search'),
)

radius_urlpatterns = patterns('heatmap.views',
	url(r'^coord/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/rad/(?P<rad>\d+(\.\d+)?)/$', 'search'),
	url(r'^coord/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/rad/(?P<rad>\d+(\.\d+)?)/', include(timestamp_urlpatterns)),
)

urlpatterns = patterns('heatmap.views',
    url(r'^search/$', 'search'),
    url(r'^search/', include(radius_urlpatterns)),
    url(r'^search/', include(timestamp_urlpatterns)),
)