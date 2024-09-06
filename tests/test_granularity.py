try:
	from django.urls import reverse
except ImportError:
	from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from collectd_rest.models import GraphGranularity, GraphGroup, Graph

class GraphGranularityTest(TestCase):
	def setUp(self):
		self.client = APIClient()

	def test_granularity_create1(self):
		url = reverse('graphgranularity-list')
		response = self.client.post(url, {
			'name': 'custom',
			'max_age': 42}, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		granularity = GraphGranularity.objects.get(name="custom")
		self.assertEqual(granularity.max_age, 42)
	def test_granularity_create2(self):
		url = reverse('graphgranularity-list')
		# name is missed here
		response = self.client.post(url, {
			'max_age': 42}, format='json')
		# max_age is missed here
		response = self.client.post(url, {
			'name': 'custom'}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	def test_granularity_create3(self):
		url = reverse('graphgranularity-list')
		# default is always exists
		response = self.client.post(url, {
			'name': 'default',
			'max_age': 42}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
