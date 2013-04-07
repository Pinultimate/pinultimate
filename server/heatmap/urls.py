from django.conf.urls import patterns, include, url

'''
timestamp_urlpatterns = patterns('heatmap.views.raw',
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'search'),
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/$', 'search'),
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/$', 'search'),
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/&callback=(?P<callback>jQuery[\d_]+)/$', 'search'),
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/&callback=(?P<callback>jQuery[\d_]+)/$', 'search'),
	url(r'^ts/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/&callback=(?P<callback>jQuery[\d_]+)/$', 'search'),
)

normalized_urlpatterns = patterns('heatmap.views.normalized',
	url(r'^search/$', 'search'),
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

    url(r'^normalized/', include(normalized_urlpatterns)),
)
'''


raw_query_timerange_urlpatterns('heatmap.views.raw',
	url(r'from/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/$', 'search_region_to_now'),
	url(r'from/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/&callback=(?P<callback>jQuery[\d_]+)/$', 'search_region_to_now'),
	url(r'from/(?P<fyear>\d+)/(?P<fmonth>\d+)/(?P<fday>\d+)/(?P<fhour>\d+)/to/(?P<tyear>\d+)/(?P<tmonth>\d+)/(?P<tday>\d+)/(?P<thour>\d+)/$', 'search_region_in_timeframe'),
	url(r'from/(?P<fyear>\d+)/(?P<fmonth>\d+)/(?P<fday>\d+)/(?P<fhour>\d+)/to/(?P<tyear>\d+)/(?P<tmonth>\d+)/(?P<tday>\d+)/(?P<thour>\d+)/&callback=(?P<callback>jQuery[\d_]+)/$', 'search_region_in_timeframe'),
)

raw_query_urlpatterns('heatmap.views.raw',
	url(r'search/$', 'search'),
	url(r'search/&callback=(?P<callback>jQuery[\d_]+)/$', 'search'),
	url(r'search/center/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/region/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/$', 'search_region'),
	url(r'search/center/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/region/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/&callback=(?P<callback>jQuery[\d_]+)/$', 'search_region'),
	url(r'search/center/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/region/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/', include(raw_query_timerange_urlpatterns)),
)

grid_query_timerange_urlpatterns('heatmap.views.normalized',
	url(r'from/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/$', 'grid_search_region_to_now'),
	url(r'from/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/&callback=(?P<callback>jQuery[\d_]+)/$', 'grid_search_region_to_now'),
	url(r'from/(?P<fyear>\d+)/(?P<fmonth>\d+)/(?P<fday>\d+)/(?P<fhour>\d+)/to/(?P<tyear>\d+)/(?P<tmonth>\d+)/(?P<tday>\d+)/(?P<thour>\d+)/$', 'grid_search_region_in_timeframe'),
	url(r'from/(?P<fyear>\d+)/(?P<fmonth>\d+)/(?P<fday>\d+)/(?P<fhour>\d+)/to/(?P<tyear>\d+)/(?P<tmonth>\d+)/(?P<tday>\d+)/(?P<thour>\d+)/&callback=(?P<callback>jQuery[\d_]+)/$', 'grid_search_region_in_timeframe'),
)

grid_query_urlpatterns('heatmap.views.normalized',
	url(r'search/$', 'grid_search'),	
	url(r'search/&callback=(?P<callback>jQuery[\d_]+)/$', 'grid_search'),
	url(r'search/center/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/region/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/$', 'grid_search_region'),
	url(r'search/center/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/region/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/&callback=(?P<callback>jQuery[\d_]+)/$', 'grid_search_region'),
	url(r'search/center/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/region/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/', include(grid_query_timerange_urlpatterns)),
)

urlpatterns = patterns('',
	url(r'^raw/', include(raw_query_urlpatterns)),
	url(r'^grid/', include(grid_query_urlpatterns)),
)
