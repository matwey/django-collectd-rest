from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from collectd_rest.models import Graph, GraphGroup
from unittest.mock import patch, create_autospec
import collectd_rest.models

class GraphTest(TestCase):
	def setUp(self):
		self.client = APIClient()

	@patch('collectd_rest.models.render')
	def test_graph_create(self, mock):
		command = 'format'
		format = 'PNG'

		url = reverse('graph-list')
		group = GraphGroup.objects.create(name="group1", title="Group 1")
		response = self.client.post(url, {
			'title': 'New Graph',
			'name': 'graph1',
			'group': group.pk,
			'command': command}, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		graph = Graph.objects.get(name='graph1')
		mock.assert_called_with(command, format)
