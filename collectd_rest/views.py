from collectd_rest import models, serializers, renderers
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import detail_route
from rest_framework.settings import api_settings
from django.http import HttpResponse

class GraphGroupViewSet(viewsets.ModelViewSet):
	queryset = models.GraphGroup.objects.all()
	serializer_class = serializers.GraphGroupSerializer
	lookup_field = 'name'

class GraphViewSet(viewsets.ModelViewSet):
	queryset = models.Graph.objects.all()
	serializer_class = serializers.GraphSerializer
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [renderers.PNGRenderer, ]
