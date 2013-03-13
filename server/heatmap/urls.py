from django.conf.urls import patterns, include, url


timestamp_urlpatterns = patterns('heatmap.views',
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'search'),
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/$', 'search'),
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', 'search'),
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/&callback=(?P<callback>jQuery[\d_]+)/$', 'search'),
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/&callback=(?P<callback>jQuery[\d_]+)/$', 'search'),
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/&callback=(?P<callback>jQuery[\d_]+)/$', 'search'),
)

radius_urlpatterns = patterns('heatmap.views',
	url(r'^coord/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/rad/(?P<rad>\d+(\.\d+)?)/$', 'search'),	
	url(r'^coord/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/rad/(?P<rad>\d+(\.\d+)?)/&callback=(?P<callback>jQuery[\d_]+)/$', 'search'),
	url(r'^coord/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/rad/(?P<rad>\d+(\.\d+)?)/', include(timestamp_urlpatterns)),
)

region_urlpatterns = patterns('heatmap.views',
	url(r'^coord/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/reg/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/$', 'search'),
	url(r'^coord/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/reg/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/&callback=(?P<callback>jQuery[\d_]+)/$', 'search'),
	url(r'^coord/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/reg/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/', include(timestamp_urlpatterns)),
)

urlpatterns = patterns('heatmap.views',
    url(r'^search/$', 'search'),
    url(r'^search/&callback=(?P<callback>jQuery[\d_]+)/$', 'search'),
    url(r'^search/', include(radius_urlpatterns), {'type': 'rad'}),
    url(r'^search/', include(region_urlpatterns), {'type': 'reg'}),
    url(r'^search/', include(timestamp_urlpatterns)),

    url(r'^searchexp/$', 'search', {'exp': True}),
    url(r'^searchexp/&callback=(?P<callback>jQuery[\d_]+)/$', 'search',  {'exp': True}),
    url(r'^searchexp/', include(radius_urlpatterns), {'type': 'rad', 'exp': True}),
    url(r'^searchexp/', include(region_urlpatterns), {'type': 'reg', 'exp': True}),
    url(r'^searchexp/', include(timestamp_urlpatterns), {'exp': True}),
)