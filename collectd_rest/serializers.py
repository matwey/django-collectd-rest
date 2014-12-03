from collectd_rest import models
from rest_framework import serializers

class GraphSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='graph-detail', lookup_field='name')

	class Meta:
		model = models.Graph
		fields = ('id', 'name', 'title', 'group', 'url', 'command', 'priority')

class GraphGroupSerializer(serializers.ModelSerializer):
	graphs = GraphSerializer(many=True)

	class Meta:
		model = models.GraphGroup
		fields = ('id', 'name', 'title', 'graphs')
