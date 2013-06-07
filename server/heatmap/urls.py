from django.conf.urls import patterns, include, url

raw_query_timerange_urlpatterns = patterns('heatmap.views.raw',
	url(r'from/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/$', 'search_region_to_now'),
	url(r'from/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/&callback=(?P<callback>jQuery[\d_]+)/$', 'search_region_to_now'),
	url(r'from/(?P<fyear>\d+)/(?P<fmonth>\d+)/(?P<fday>\d+)/(?P<fhour>\d+)/to/(?P<tyear>\d+)/(?P<tmonth>\d+)/(?P<tday>\d+)/(?P<thour>\d+)/$', 'search_region_in_timeframe'),
	url(r'from/(?P<fyear>\d+)/(?P<fmonth>\d+)/(?P<fday>\d+)/(?P<fhour>\d+)/to/(?P<tyear>\d+)/(?P<tmonth>\d+)/(?P<tday>\d+)/(?P<thour>\d+)/&callback=(?P<callback>jQuery[\d_]+)/$', 'search_region_in_timeframe'),
)

raw_query_urlpatterns = patterns('heatmap.views.raw',
	url(r'search/$', 'search'),
	url(r'search/&callback=(?P<callback>jQuery[\d_]+)/$', 'search'),
	url(r'search/center/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/region/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/$', 'search_region'),
	url(r'search/center/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/region/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/&callback=(?P<callback>jQuery[\d_]+)/$', 'search_region'),
	url(r'search/center/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/region/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/', include(raw_query_timerange_urlpatterns)),
)

grid_query_timerange_urlpatterns = patterns('heatmap.views.grid',
	url(r'from/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/$', 'grid_search_region_to_now'),
	url(r'from/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/&callback=(?P<callback>jQuery[\d_]+)/$', 'grid_search_region_to_now'),
	url(r'from/(?P<fyear>\d+)/(?P<fmonth>\d+)/(?P<fday>\d+)/(?P<fhour>\d+)/to/(?P<tyear>\d+)/(?P<tmonth>\d+)/(?P<tday>\d+)/(?P<thour>\d+)/$', 'grid_search_region_in_timeframe'),
	url(r'from/(?P<fyear>\d+)/(?P<fmonth>\d+)/(?P<fday>\d+)/(?P<fhour>\d+)/to/(?P<tyear>\d+)/(?P<tmonth>\d+)/(?P<tday>\d+)/(?P<thour>\d+)/&callback=(?P<callback>jQuery[\d_]+)/$', 'grid_search_region_in_timeframe'),
)

grid_query_urlpatterns = patterns('heatmap.views.grid',
	url(r'search/$', 'grid_search'),
	url(r'search/&callback=(?P<callback>jQuery[\d_]+)/$', 'grid_search'),
	url(r'search/center/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/region/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/$', 'grid_search_region'),
	url(r'search/center/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/region/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/&callback=(?P<callback>jQuery[\d_]+)/$', 'grid_search_region'),
	url(r'search/center/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/region/(?P<latrange>\d+(\.\d+)?)/(?P<lonrange>\d+(\.\d+)?)/', include(grid_query_timerange_urlpatterns)),
)

tweets_urlpatterns = patterns('heatmap.views.tweets',
	url(r'center/(?P<lat>[+-]?\d+(\.\d+)?)/(?P<lon>[+-]?\d+(\.\d+)?)/radius/(?P<radius>\d+(\.\d+)?)/from/(?P<fyear>\d+)/(?P<fmonth>\d+)/(?P<fday>\d+)/(?P<fhour>\d+)/to/(?P<tyear>\d+)/(?P<tmonth>\d+)/(?P<tday>\d+)/(?P<thour>\d+)/$', 'twitter_reverse_geocode'),
)

urlpatterns = patterns('',
	url(r'raw/', include(raw_query_urlpatterns)),
	url(r'resolution/(?P<resolution>\d+(\.\d+)?)/', include(grid_query_urlpatterns)),
	url(r'tweets/', include(tweets_urlpatterns)),
)
