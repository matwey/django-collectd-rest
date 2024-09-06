try:
	from django.urls import reverse
except ImportError:
	from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from collectd_rest.models import Graph, GraphGroup, GraphGranularity

class GraphGroupTest(TestCase):
	def setUp(self):
		self.client = APIClient()
	
	def test_group_create1(self):
		url = reverse('graphgroup-list')
		response = self.client.post(url, {
			'title': "The Group",
			'name': 'group1'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		group1 = GraphGroup.objects.get(name="group1")
	def test_group_create2(self):
		url = reverse('graphgroup-list')
		# title is missed here
		response = self.client.post(url, {
			'name': 'group2'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		# name is missed here
		response = self.client.post(url, {
			'title': 'The Group'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	def test_group_list1(self):
		group = GraphGroup.objects.create(name="group1", title="Group 1")
		granularity = GraphGranularity.objects.get(name='default')
		graph = Graph.objects.create(name="graph1", title="Graph 1", command="format", group=group, granularity=granularity)

		url = reverse('graphgroup-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		json = response.json()
		self.assertEqual(len(json), 1)
