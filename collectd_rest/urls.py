from collectd_rest import views
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'granularities', views.GraphGranularityViewSet)
router.register(r'groups', views.GraphGroupViewSet)
router.register(r'graphs', views.GraphViewSet)

urlpatterns = [
	url(r'^', include(router.urls)),
]
