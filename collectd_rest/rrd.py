import shlex, subprocess

class RRDError(Exception):
	def __init__(self, message):
		self.message = message

def render(command, format):
	args = ['rrdtool','graph','-','--imgformat',format] + shlex.split(command)
	p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	code = p.wait()
	if code != 0:
		raise RRDError(p.stderr.read())
	return p.stdout.read()
