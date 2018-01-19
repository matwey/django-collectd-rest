from collectd_rest import models, serializers, renderers
from rest_framework import viewsets
from rest_framework.settings import api_settings

class GraphGranularityViewSet(viewsets.ModelViewSet):
	queryset = models.GraphGranularity.objects.all()
	serializer_class = serializers.GraphGranularitySerializer
	lookup_field = 'name'

class GraphGroupViewSet(viewsets.ModelViewSet):
	queryset = models.GraphGroup.objects.all()
	serializer_class = serializers.GraphGroupSerializer
	lookup_field = 'name'

class GraphViewSet(viewsets.ModelViewSet):
	queryset = models.Graph.objects.prefetch_related('granularity').all()
	serializer_class = serializers.GraphSerializer
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [renderers.PNGRenderer, renderers.SVGRenderer, ]
