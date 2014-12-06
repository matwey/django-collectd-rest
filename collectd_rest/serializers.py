from collectd_rest import models
from rest_framework import serializers

class GraphSerializer(serializers.ModelSerializer):
	group = serializers.SlugRelatedField(slug_field='name')
	url = serializers.HyperlinkedIdentityField(view_name='graph-detail', lookup_field='name')

	class Meta:
		model = models.Graph
		fields = ('id', 'name', 'title', 'group', 'url', 'command', 'priority')

	def validate(self, attrs):
		instance = GraphSerializer.Meta.model(**attrs)
		instance.clean()
		return attrs

class GraphGroupSerializer(serializers.ModelSerializer):
	graphs = GraphSerializer(many=True, read_only=True)

	class Meta:
		model = models.GraphGroup
		fields = ('id', 'name', 'title', 'graphs')
