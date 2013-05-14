from django.conf.urls import patterns, include, url

urlpatterns = patterns('analytics.views',
	url(r'create/(?P<username>[a-zA-Z0-9]{15})/$', 'create_user'),
	url(r'login/(?P<username>[a-zA-Z0-9]{15})/$', 'user_login'),
	url(r'logout/((?P<username>[a-zA-Z0-9]{15}))/$', 'user_logout'),
	url(r'tap/((?P<username>[a-zA-Z0-9]{15}))/$', 'user_touch'),
)
