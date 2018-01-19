import rrdtool
import shlex

def render(command, format):
	format = format.upper()
	args = ['--imgformat',format] + shlex.split(command)
	graph = rrdtool.graphv('-', *args)
	return graph['image']
