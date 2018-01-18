from collectd_rest.rrd import render
from django.db import models

class GraphGroup(models.Model):
	name = models.SlugField(max_length=256, blank = False, unique = True)
	title = models.CharField(max_length=256, blank = False)

	def __repr__(self):
		return '<GraphGroup %s>' % self.name

class Graph(models.Model):
	name = models.SlugField(max_length=256, blank = False)
	title = models.CharField(max_length=256, blank = True)
	priority = models.IntegerField(default=0)
	group = models.ForeignKey('GraphGroup', on_delete=models.CASCADE, related_name='graphs')
	command = models.TextField(blank = False)

	class Meta:
		unique_together = ("name", "group")
		ordering = ['-priority']

	def render(self, format):
		return render(self.command, format)

	def __repr__(self):
		return '<Graph %s in %s>' % (self.name, self.group.name)
