from collectd_rest import models
from collectd_rest.rrd import render, RRDError
from rest_framework import serializers

class CommandField(serializers.CharField):
	def __init__(self, *args, **kwargs):
		super(CommandField,self).__init__(*args, **kwargs)
	def run_validation(self, data):
		data = super(CommandField,self).run_validation(data)
		try:
			render(data, "PNG")
		except RRDError as e:
			raise serializers.ValidationError(e.message)
		return data

class GraphSerializer(serializers.ModelSerializer):
	group = serializers.SlugRelatedField(slug_field='name', queryset=models.GraphGroup.objects.all(), required=True)
	url = serializers.HyperlinkedIdentityField(view_name='graph-detail', read_only=True)
	command = CommandField()

	class Meta:
		model = models.Graph
		fields = ('id', 'name', 'title', 'group', 'url', 'command', 'priority')

class GraphGroupSerializer(serializers.ModelSerializer):
	graphs = GraphSerializer(many=True, read_only=True)

	class Meta:
		model = models.GraphGroup
		fields = ('id', 'name', 'title', 'graphs')
