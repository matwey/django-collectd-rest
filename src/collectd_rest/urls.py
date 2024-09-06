from collectd_rest import views
from rest_framework.routers import DefaultRouter
import django

router = DefaultRouter()
router.register(r'granularities', views.GraphGranularityViewSet)
router.register(r'groups', views.GraphGroupViewSet)
router.register(r'graphs', views.GraphViewSet)

if django.VERSION[0] > 1:
	from django.urls import include, re_path
else:
	from django.conf.urls import include, url as re_path

urlpatterns = [
	re_path(r'^', include(router.urls)),
]
