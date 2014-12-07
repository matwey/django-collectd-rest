import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
	'rest_framework',
	'collectd_rest',
]
REST_FRAMEWORK = {
	'DEFAULT_RENDERER_CLASSES': (
		'rest_framework.renderers.JSONRenderer',
	),
	'DEFAULT_PARSER_CLASSES': (
		'rest_framework.parsers.JSONParser',
	),
}
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': 'test.sqlite3',
	}
}
MIDDLEWARE_CLASSES = []
ROOT_URLCONF = 'tests.urls'
