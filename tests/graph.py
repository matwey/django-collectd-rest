try:
	from django.urls import reverse
except ImportError:
	from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from collectd_rest.models import Graph, GraphGroup
from collectd_rest.rrd import RRDError
try:
	from unittest.mock import patch, create_autospec
except ImportError:
	from mock import patch, create_autospec

class GraphTest(TestCase):
	def setUp(self):
		self.client = APIClient()

	@patch('collectd_rest.serializers.render')
	def test_graph_create1(self, mock):
		command = 'format'
		format = 'PNG'

		url = reverse('graph-list')
		group = GraphGroup.objects.create(name="group1", title="Group 1")
		response = self.client.post(url, {
			'title': 'New Graph',
			'name': 'graph1',
			'group': group.name,
			'command': command}, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		graph = Graph.objects.get(name='graph1')
		mock.assert_called_with(command, format)
	@patch('collectd_rest.serializers.render')
	def test_graph_create2(self, mock):
		command = 'format'
		format = 'png'

		url = reverse('graph-list')
		group = GraphGroup.objects.create(name="group1", title="Group 1")
		# name is missed here
		response = self.client.post(url, {
			'title': 'New Graph',
			'group': group.name,
			'command': command}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		# title may be missed here
		response = self.client.post(url, {
			'name': 'graph2',
			'group': group.name,
			'command': command}, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		graph = Graph.objects.get(name='graph2')
		self.assertEqual(graph.title, "")
		# group is missed here
		response = self.client.post(url, {
			'title': 'New Graph',
			'name': 'graph3',
			'command': command}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	def test_graph_create3(self):
		url = reverse('graph-list')
		group = GraphGroup.objects.create(name="group1", title="Group 1")
		# command is missed here
		response = self.client.post(url, {
			'title': 'New Graph',
			'name': 'graph1',
			'group': group.name}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	@patch('collectd_rest.serializers.render')
	def test_graph_create_duplicates(self, mock):
		command = 'format'
		format = 'png'

		url = reverse('graph-list')
		group1 = GraphGroup.objects.create(name="group1", title="Group 1")
		group2 = GraphGroup.objects.create(name="group2", title="Group 2")
		response = self.client.post(url, {
			'title': 'New Graph',
			'name': 'graph',
			'group': group1.name,
			'command': command}, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		response = self.client.post(url, {
			'title': 'New Graph',
			'name': 'graph',
			'group': group1.name,
			'command': command}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		response = self.client.post(url, {
			'title': 'New Graph',
			'name': 'graph',
			'group': group2.name,
			'command': command}, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(len(Graph.objects.filter(name='graph')),2)

	def graph_render_helper(self, mock, mime, format):
		command = 'format'

		group = GraphGroup.objects.create(name="group1", title="Group 1")
		graph = Graph.objects.create(name="graph1", title="Graph 1", command = command, group=group)
		url = reverse('graph-detail', args=[graph.id])
		response = self.client.get(url, HTTP_ACCEPT=mime)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response["Content-Type"], mime)
		mock.assert_called_with(command, format)

	@patch('collectd_rest.serializers.render')
	def test_graph_render_png(self, mock):
		format = 'png'
		mime = "image/png"
		self.graph_render_helper(mock, mime, format)

	@patch('collectd_rest.serializers.render')
	def test_graph_render_svg(self, mock):
		format = 'svg'
		mime = "image/svg+xml"
		self.graph_render_helper(mock, mime, format)

	@patch('collectd_rest.serializers.render')
	def test_graph_validate1(self, mock):
		mock.side_effect = RRDError('Boom!')
		command = "wrong command"

		url = reverse('graph-list')
		group = GraphGroup.objects.create(name="group1", title="Group 1")
		response = self.client.post(url, {
			'title': 'New Graph',
			'name': 'graph1',
			'group': group.name,
			'command': command}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.content,b"{\"command\":[\"Boom!\"]}")
