import shlex, subprocess

class RRDError(Exception):
	def __init__(self, message):
		self.message = message

def render(command, format):
	format = format.upper()
	args = ['rrdtool','graph','-','--imgformat',format] + shlex.split(command)
	p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	outs, errs = p.communicate()
	if p.returncode != 0:
		raise RRDError(errs)
	return outs
