from django.conf.urls import patterns, include, url

urlpatterns = patterns('analytics.views',
	url(r'user/()/login/$', 'user_login'),
	url(r'user/()/logout/$', 'user_logout'),
	url(r'user/()/touch/$', 'user_touch'),
)
