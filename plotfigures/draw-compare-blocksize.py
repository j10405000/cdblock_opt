#!/usr/bin/env python
import sys, os
from data import *

datasets = [web40, web200, web400, web1000]


if len(sys.argv) > 2:
	print('[Usage] ./draw-compare-blocksize.py [logdir]')
	exit(1)
elif len(sys.argv) == 2:
	logdir = sys.argv[1]
else:
	logdir = '../log'

FILETYPE = ['png','eps']
#Add more colors
COLORS = 'b,k,g,r,c,m,y,blueviolet,lightgreen,'.split(',')
COLORS = 'blue,black,green,red,cyan,magenta,chartreuse,blueviolet,forestgreen,black,aqua'.split(',')
LINESTYLES = '-,-.,--,:'.split(',')
MARKERS = '.,o,v,^,*,+,x,s'.split(',')
mycolor = lambda i: COLORS[i%len(COLORS)]
mylinestyle = lambda i: LINESTYLES[i%len(LINESTYLES)]
mymarker = lambda i: MARKERS[i%len(MARKERS)]

def existlog(log):
	if not os.path.exists(log):
		print('%s does not exist. Cannot draw it.' % log)
		return False
	else:
		return True

def getcoordinates():
	times, objectives= {}, {}
	for data in datasets:
		times[data], objectives[data] = [], []
		timelog = os.path.join(logdir,'time/%s#BLOCK-L-D' % data.name)
		if not existlog(timelog):
			exit(1)
		for line in open(timelog):
			line = line.strip()
			if line == '' or line[0] == '$' or 'iter' not in line:
				continue
			pt = dict(zip(line.split()[::2],line.split()[1::2]))
			times[data] += [float(pt['time'])]
			# relative dual obj, dual optimal = - primal optimal
			objectives[data] += [abs((float(pt['obj'])+data.primal)/data.primal)]

		# shift initial data loading/preprocessing time
	 	timeshift = data.time
		times[data] = [t+timeshift for t in times[data]]
	return times, objectives

#Draw now!
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('text',usetex=True)
matplotlib.rc('font',family='serif',size='14')
matplotlib.rc(('xtick.major'), pad = 9)
from matplotlib import pylab

times, objectives = getcoordinates()
pylab.figure()
for i,data in enumerate(datasets):
	pylab.plot(times[data], objectives[data], label='$m = %s$' % data.blocks, lw=3, c=mycolor(i), ls=mylinestyle(i))
pylab.xlim([2000,4000])
pylab.legend(loc='best')
pylab.xlabel('Time (sec.)')
pylab.ylabel('Relative function value difference')
if not os.path.exists('figures'):
	os.mkdir('figures')
for fmt in FILETYPE:
	pylab.savefig('figures/web.compare.blocksize.obj'+'.'+fmt)


