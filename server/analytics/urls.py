from django.conf.urls import patterns, include, url

analytics_urlpatterns = patterns('analytics.views.user',
	url(r'new_user/$', 'new_user'),
)

urlpatterns = patterns('',
	url(r'', include(analytics_urlpatterns)),
)
