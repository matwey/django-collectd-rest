#!/usr/bin/env python
import os
import sys

def runtests():
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.test_settings")

	try:
		from django import setup
		setup()
	except ImportError:
		pass
	from django.core.management import call_command

	call_command("test", "tests.__init__", verbosity=2)

if __name__ == "__main__":
	runtests()
