import django

if django.VERSION[0] > 1:
	from django.urls import include, re_path
else:
	from django.conf.urls import include, url as re_path

urlpatterns = [
	re_path(r'', include('collectd_rest.urls')),
]
