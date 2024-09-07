from collectd_rest import models, serializers, renderers
from rest_framework import viewsets
from rest_framework.settings import api_settings
from django.contrib.auth.models import AnonymousUser

class GraphGranularityViewSet(viewsets.ModelViewSet):
	queryset = models.GraphGranularity.objects.all()
	serializer_class = serializers.GraphGranularitySerializer
	lookup_field = 'name'

class GraphGroupViewSet(viewsets.ModelViewSet):
	queryset = models.GraphGroup.objects.prefetch_related('graphs', 'graphs__granularity')
	serializer_class = serializers.GraphGroupSerializer
	lookup_field = 'name'

class GraphViewSet(viewsets.ModelViewSet):
	queryset = models.Graph.objects.select_related('granularity')
	serializer_class = serializers.GraphSerializer
	unauthenticated_serializer_class = serializers.UnauthenticatedGraphSerializer
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES + [renderers.PNGRenderer, renderers.SVGRenderer, ]

	def get_serializer_class(self):
		if (not (self.action == "retrieve" or self.action == "list")
			or isinstance(self.request.accepted_renderer, renderers.ImageRenderer)
			or not isinstance(self.request.user, AnonymousUser)):

			return super(GraphViewSet, self).get_serializer_class()

		return self.unauthenticated_serializer_class
