import shlex, subprocess

def render(command, format):
	args = ['rrdtool','graph','-','--imgformat',format] + shlex.split(command)
	p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	code = p.wait()
	if code != 0:
		raise subprocess.CalledProcessError(code, p.args, p.stderr.read())
	return p.stdout.read()
