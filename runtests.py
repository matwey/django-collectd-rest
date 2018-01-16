#!/usr/bin/env python
import os

def runtests():
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.test_settings")

	try:
		from django import setup
		setup()
	except ImportError:
		pass
	from django.core.management import call_command

	os.sys.exit(call_command("test", "tests.test_all", verbosity=2))

if __name__ == "__main__":
	runtests()
