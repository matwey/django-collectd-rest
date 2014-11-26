from rest_framework import renderers
from collectd_rest.rrd import render

class PNGRenderer(renderers.BaseRenderer):
	media_type = 'image/png'
	format = 'png'
	charset = None
	render_style = 'binary'
	
	def render(self, data, media_type=None, renderer_context=None):
		command = data['command']
		return render(command, 'PNG')
