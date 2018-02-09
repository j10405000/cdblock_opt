#!/usr/bin/env python
import sys, os
from data import *

datasets = [web40, web200, web400, web1000]

if len(sys.argv) > 2:
	print('[Usage] ./draw-compare-perm.py [logdir]')
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

def getcoordinate(data, logsuffix):
	timelog = os.path.join(logdir,'time/%s#BLOCK-L-D%s' % (data.name, logsuffix))
	if not existlog(timelog):
		exit(1)
	time, objective = [], []
	for line in open(timelog):
		line = line.strip()
		if line == '' or line[0] == '$' or 'iter' not in line:
			continue
		pt = dict(zip(line.split()[::2],line.split()[1::2]))
		time += [float(pt['time'])]
		# relative dual obj, dual optimal = - primal optimal
		objective += [abs((float(pt['obj'])+data.primal)/data.primal)]

	# shift initial data loading/preprocessing time
	timeshift = data.time
	time = [t+timeshift for t in time]
	return time, objective

def draw_onecurve(data, logsuffix, label, idx):
	x, y = getcoordinate(data, logsuffix)
	pylab.plot(x,y,label=label, lw=3, c=mycolor(idx), ls=mylinestyle(idx))

#Draw now!
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('text',usetex=True)
matplotlib.rc('font',family='serif',size='14')
matplotlib.rc(('xtick.major'), pad = 9)
from matplotlib import pylab

pylab.figure()
draw_onecurve(webraw40,'#np','raw+noperm',0)
draw_onecurve(webraw40,'','raw+perm',1)
draw_onecurve(web40,'#np','noperm',2)
draw_onecurve(web40,'','perm',3)
pylab.xlim([2000,3000])
pylab.legend(loc='best')
pylab.xlabel('Time (sec.)')
pylab.ylabel('Relative function value difference')
if not os.path.exists('figures'):
	os.mkdir('figures')
for fmt in FILETYPE:
	pylab.savefig('figures/web.compare.perm.obj'+'.'+fmt)

