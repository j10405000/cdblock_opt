#!/usr/bin/env python
import sys,os
from data import *

datasets = [leisure5, web40, epsilon30, kdd40]
datasets = [web40, epsilon30, kdd40]

solvers = ['BLOCK-L-10','VW']


if len(sys.argv) > 2:
	print('[Usage] ./draw-compare-block-vw-bestC.py [logdir]')
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
		print('\t%s does not exist.' % log)
		return False
	else:
		return True

withoutlog = False
def getcoordinates(data):
	global withoutlog
	withoutlog = False
	times, accuracys = {}, {}
	for solver in solvers:
		times[solver], accuracys[solver] = [], []
		timelog = os.path.join(logdir,'time/%s#%s_bestC' % (data.name, solver))
		acclog = os.path.join(logdir,'acc/%s#%s_bestC.acc' % (data.name, solver))
		if not existlog(timelog) or not existlog(acclog):
			withoutlog = True
			return times, accuracys

		primal, accuracy, iters = {}, {}, []
		liblinear_loadtime = 0
		for line in open(acclog):
			line = line.strip()
			if line == '' or line[0] == '$' or 'iter' not in line or 'accuracy' not in line:
				print 'skip %s' %line
				continue
			pt = dict(zip(line.split()[::2],line.split()[1::2]))
			#primal[pt['iter']] = float(pt['primal'])
			accuracy[pt['iter']] = float(pt['accuracy'])	
		for line in open(timelog):
			line = line.strip()
			if line == '' or line[0] == '$' or 'iter' not in line:
				print 'skip %s' %line
				continue
			pt = dict(zip(line.split()[::2],line.split()[1::2]))
			if pt['iter'] == '0':
				liblinear_loadtime = float(pt['time'])
			elif '.' in pt['iter']:
				continue
			elif pt['iter'] in accuracy:
				#transform to reletive primal value
				times[solver] += [float(pt['time'])]
				accuracys[solver] += [accuracy[pt['iter']]]
		if solver == 'STREAMSVM':
			print data.name
			print times[solver]
			print accuracys[solver]
		# shift initial data loading/preprocessing time
		timeshift = 0
		if solver.startswith('BLOCK'):  timeshift = data.time
		elif solver.startswith('VW'): timeshift = data.vwtime
		elif solver.startswith('LIBLINEAR'): timeshift = liblinear_loadtime
		print solver, timeshift
		times[solver] = [t+timeshift for t in times[solver]]
	for solver in solvers:
		#accuracys[solver] = [abs((acc-bestacc)/bestacc) for acc in accuracys[solver]]
		accuracys[solver] = [100*acc for acc in accuracys[solver]]
	return times,  accuracys

def draw(drawer, x, y, xlabel, ylabel, filename, vline_x=0, legloc='best', xlim=None, ylim=None, otherfunc=None):
	pylab.figure()
	params = {'axes.labelsize': 16, 'text.fontsize': 16, 'legend.fontsize': 20,'xtick.labelsize': 20,'ytick.labelsize': 20}
	pylab.rcParams.update(params)
	for i,solver in enumerate(solvers):
		if solver != 'STREAMSVM':
			drawer(x[solver], y[solver], label=solver, lw=3, c=mycolor(i), ls=mylinestyle(i)) #, marker=mymarker(i))
	pylab.xlabel(xlabel.replace('_','\_'))
	pylab.ylabel(ylabel.replace('_','\_'))
	pylab.legend(loc=legloc)
	if xlim: pylab.xlim(xlim)
	if ylim: pylab.ylim(ylim)
	if vline_x: pylab.axvline(x=vline_x,linestyle='dotted',color='b')
	if otherfunc: otherfunc()
	if not os.path.exists('figures'):
		os.mkdir('figures')
	for fmt in FILETYPE:
		pylab.savefig('figures/%s_bestC.%s'%(filename,fmt))

def addstreamsvm(x0, y0, x1,y1,x2,y2, bestacc, time, acc):
	pylab.text(x0,y0, r'{\bf Best Acc.: %.5s\%%}' %(bestacc))
	pylab.text(x1,y1,'{\sf StreamSVM}')
	pylab.text(x2,y2,'%.5s\%%/%5s sec.' % (bestacc-acc, time))

#Draw now!
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('text',usetex=True)
matplotlib.rc('font',family='serif',size='12')
matplotlib.rc(('xtick.major'), pad = 9)
from matplotlib import pylab

for data in datasets:
	times, accuracys = getcoordinates(data)
	if withoutlog:
		print('Witout enough log to draw figure for %s.' % (data.name))
		continue
	vline_x, xlim, otherfunc  = data.time, None, None
	ylim = None
	if data.name.startswith('web'): 
		xlim = [700, 10**4]
		x0, y0, x1, y1, x2, y2 = 3*10**4, 10**0, 3*10**4, 10**-0.2, 3*10**4, 10**-0.4
	elif data.name.startswith('eps'):
		xlim = [10**3, 10**4]
		x0, y0, x1, y1, x2, y2 = 3.3*10**4, 10**0.5, 3.3*10**4, 10**0.4, 3.3*10**4, 10**0.3
	elif data.name.startswith('leisure'):
		xlim = [10**2, 2*10**3]
		x0, y0, x1, y1, x2, y2 = 1.8*10**4, 10**-0.4, 1.8*10**4, 10**-0.6, 1.8*10**4, 10**-0.8
	elif data.name.startswith('kdd'):
		xlim = [400,10000]
		x0, y0, x1, y1, x2, y2 = 1.8*10**4, 10**-0.4, 1.8*10**4, 10**-0.6, 1.8*10**4, 10**-0.8
	if 'STREAMSVM' in solvers:
		time,acc = times['STREAMSVM'][0], accuracys['STREAMSVM'][0]
		otherfunc = lambda : addstreamsvm(x0, y0, x1, y1, x2, y2, bestacc, time, acc)

	draw(pylab.semilogx, times, accuracys, 'Time (sec.)', 'Accuracy (\%)',\
			#'%s.compare.solvers.acc'%data.name, data.time, 'center right', xlim, None,\
			'%s.compare.solvers.acc'%data.name, data.time, 'best', xlim, ylim,\
			otherfunc)

