from collectd_rest.rrd import render, RRDError
from django.db import models
from django.core.exceptions import ValidationError

class GraphGroup(models.Model):
	name = models.CharField(max_length=256, blank = False, null = True, unique = True)
	title = models.CharField(max_length=256)

class Graph(models.Model):
	name = models.CharField(max_length=256, blank = False, null = True)
	title = models.CharField(max_length=256)
	priority = models.IntegerField(default=0)
	group = models.ForeignKey('GraphGroup', related_name='graphs')
	command = models.TextField(blank = False, null = True)

	class Meta:
		unique_together = ("name", "group")
		ordering = ['-priority']

	def clean(self):
		try:
			render(self.command, 'PNG')
		except RRDError as e:
			raise ValidationError({'command':e.message})

