import os
import sys
from setuptools import setup, Extension

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
	README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

rrd = Extension('collectd_rest.rrd',
	sources = ['rrd.c'],
	libraries = ['rrd'])

setup(
	name='django-collectd-rest',
	version='0.2.1',
	packages=['collectd_rest', 'collectd_rest.migrations'],
	ext_modules=[rrd],
	include_package_data=True,
	license='BSD-2-Clause',
	description='A simple Django application to demonstrate RRD plots generated by collectd or any other rrd data',
	long_description=README,
	long_description_content_type="text/markdown",
	url='https://github.com/matwey/django-collectd-rest',
	author='Matwey V. Kornilov',
	author_email='matwey.kornilov@gmail.com',
	classifiers=[
		'Environment :: Web Environment',
		'Framework :: Django',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Topic :: Internet :: WWW/HTTP',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	],
	test_suite='runtests.runtests'
)
