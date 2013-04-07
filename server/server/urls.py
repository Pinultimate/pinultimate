from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^heatmap/', include('heatmap.urls')),
    (r'^instagram/subscription/', 'instagram.views.subscription'),
)
