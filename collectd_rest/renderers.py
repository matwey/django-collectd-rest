from django.utils.cache import patch_cache_control
from rest_framework import renderers, status

class ImageRenderer(renderers.BaseRenderer):
	charset = None
	render_style = 'binary'

	def render(self, data, media_type=None, renderer_context=None):
		if renderer_context is None:
			return None

		response = renderer_context['response']
		status_code = renderer_context['response'].status_code
		if not status.is_success(status_code):
			return None

		patch_cache_control(response, max_age=data['max_age'], must_revalidate=True)
		return data['command']

class PNGRenderer(ImageRenderer):
	media_type = 'image/png'
	format = 'png'
class SVGRenderer(ImageRenderer):
	media_type = 'image/svg+xml'
	format = 'svg'
