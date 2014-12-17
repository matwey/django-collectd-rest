from rest_framework import renderers
from collectd_rest.rrd import render

class ImageRenderer(renderers.BaseRenderer):
	charset = None
	render_style = 'binary'

	def render(self, data, media_type=None, renderer_context=None):
		return data['command']

class PNGRenderer(ImageRenderer):
	media_type = 'image/png'
	format = 'png'
class SVGRenderer(ImageRenderer):
	media_type = 'image/svg+xml'
	format = 'svg'
