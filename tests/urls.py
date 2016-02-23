from django.conf.urls import include, url

urlpatterns = [
	url(r'', include('collectd_rest.urls')),
]
