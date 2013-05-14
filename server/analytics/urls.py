from django.conf.urls import patterns, url

urlpatterns = patterns('analytics.views',
	url(r'^tap/$', 'tap'),
	url(r'^update/$', 'update'),
)
