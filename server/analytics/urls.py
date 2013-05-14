from django.conf.urls import patterns, include, url

urlpatterns = patterns('analytics.views',
	url(r'tap/(?P<user_id>\d+)/$', 'tap'),
	url(r'update/(?P<contact_id>\d+)/$', 'update'),
)
