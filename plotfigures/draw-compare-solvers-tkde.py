#!/usr/bin/env python
import sys,os
from data import *
solvers = ['BLOCK-L-D','BLOCK-L-1','BLOCK-L-5','BLOCK-L-10','BLOCK-L-15','BLOCK-L-20', \
		'BLOCK-P-B', 'BLOCK-P-I']#, 'LIBLINEAR', 'STREAMSVM']
solvers = ['BLOCK-L-D','BLOCK-L-1','BLOCK-L-10','BLOCK-L-20', \
		'BLOCK-P-B', 'BLOCK-P-I']#, 'LIBLINEAR', 'STREAMSVM']
datasets = [epsilon30, web40, leisure5, kdd40]
datasets = [epsilon30, web40, kdd40]
datasets = [heart_scale5]
if len(sys.argv) > 2:
	print('[Usage] ./draw-compare-solvers-tkde.py [logdir]')
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

def getcoordinates(data):
	times, primals, accuracys = {}, {}, {}
	bestacc = 0
	for solver in solvers:
		times[solver], primals[solver], accuracys[solver] = [], [], []
		timelog = logdir+'/time/%s#%s' % (data.name, solver)
		acclog = logdir+'/acc/%s#%s.acc' % (data.name, solver)
		primal, accuracy, iters = {}, {}, []
		liblinear_loadtime = 0
		for line in open(acclog):
			line = line.strip()
			if line == '' or line[0] == '$' or 'iter' not in line or 'accuracy' not in line:
				print 'skip %s' %line
				continue
			pt = dict(zip(line.split()[::2],line.split()[1::2]))
			primal[pt['iter']] = float(pt['primal'])
			accuracy[pt['iter']] = float(pt['accuracy'])	
			bestacc = max(accuracy[pt['iter']], bestacc)
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
			elif pt['iter'] in primal:
				#transform to reletive primal value
				times[solver] += [float(pt['time'])]
				primals[solver] += [abs((primal[pt['iter']]-data.primal)/data.primal)]
				accuracys[solver] += [accuracy[pt['iter']]]
		if solver == 'STREAMSVM':
			print data.name
			print times[solver]
			print accuracys[solver]
		# shift initial data loading/preprocessing time
		timeshift = 0
		if solver.startswith('BLOCK'):  timeshift = data.time
		elif solver.startswith('LIBLINEAR'): timeshift = liblinear_loadtime
		times[solver] = [t+timeshift for t in times[solver]]
	for solver in solvers:
		#accuracys[solver] = [abs((acc-bestacc)/bestacc) for acc in accuracys[solver]]
		accuracys[solver] = [100*abs((acc-bestacc)) for acc in accuracys[solver]]
	return times, primals, accuracys, 100*bestacc

def draw(drawer, x, y, xlabel, ylabel, filename, vline_x=0, legloc='best', xlim=None, ylim=None, otherfunc=None):
	pylab.figure()
	params = {'font.size': 16, 'axes.labelsize': 16, 'text.fontsize': 16, 'legend.fontsize': 16,'xtick.labelsize': 20,'ytick.labelsize': 20}
	pylab.rcParams.update(params)
	for i,solver in enumerate(solvers):
		if solver != 'STREAMSVM':
			drawer(x[solver], y[solver], label=solver, lw=5, c=mycolor(i), ls=mylinestyle(i)) #, marker=mymarker(i))
	pylab.xlabel(xlabel.replace('_','\_'), fontsize='large')
	pylab.ylabel(ylabel.replace('_','\_'), fontsize='large')
	pylab.legend(loc=legloc)
	if xlim: pylab.xlim(xlim)
	if ylim: pylab.ylim(ylim)
	if vline_x: pylab.axvline(x=vline_x,linestyle='dotted',color='b',lw=5)
	if otherfunc: otherfunc()
	if not os.path.exists('figures'):
		os.mkdir('figures')
	for fmt in FILETYPE:
		pylab.savefig('figures/%s.%s'%(filename,fmt))

def addstreamsvm(x0, y0, x1,y1,x2,y2, bestacc, time, acc):
	pylab.text(x0,y0, r'{\bf Best Acc.: %.5s\%%}' %(bestacc),fontsize=16)
#	pylab.text(x0,y0, r'{\bf Best Acc.: %.5s\%%}' %(bestacc))
#	pylab.text(x1,y1,'{\sf StreamSVM}')
#	pylab.text(x2,y2,'%.5s\%%/%5s sec.' % (bestacc-acc, time))

#Draw now!
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('text',usetex=True)
matplotlib.rc('font',family='serif',size='12')
matplotlib.rc(('xtick.major'), pad = 9)
from matplotlib import pylab

for data in datasets:
	times, primals, accuracys, bestacc = getcoordinates(data)
	vline_x, xlim, otherfunc  = data.time, None, None
	if data.name.startswith('web'): 
		xlim = [10**3, 10**4]
		x0, y0, x1, y1, x2, y2 = 4.8*10**3, 1.2*10**0, 3*10**4, 10**-0.2, 3*10**4, 10**-0.4
	elif data.name.startswith('eps'):
		xlim = [10**3, 10**4]
		x0, y0, x1, y1, x2, y2 = 4.8*10**3, 4*0.1, 3.3*10**4, 10**0.4, 3.3*10**4, 10**0.3
	elif data.name.startswith('leisure'):
		xlim = [2*10**2, 10**3]
		x0, y0, x1, y1, x2, y2 = 6*10**2, 4*0.1, 1.8*10**4, 10**-0.6, 1.8*10**4, 10**-0.8
	elif data.name.startswith('kdd'):
		x0, y0, x1, y1, x2, y2 = 1.1*10**4, 1.1, 1.8*10**4, 10**-0.6, 1.8*10**4, 10**-0.8

	if 'STREAMSVM' in solvers:
		time,acc = times['STREAMSVM'][0], accuracys['STREAMSVM'][0]
		otherfunc = lambda : addstreamsvm(x0, y0, x1, y1, x2, y2, bestacc, time, acc)

	draw(pylab.loglog, times, primals, 'Time (sec.)', 'Relative function value difference',\
			'%s.compare.solvers.tkde.obj'%data.name, data.time, 'best', xlim,None,None)

	otherfunc = lambda : addstreamsvm(x0, y0, x1, y1, x2, y2, bestacc, 0, 0)
	draw(pylab.loglog, times, accuracys, 'Time (sec.)', 'Difference to the best accuracy (\%)',\
			#'%s.compare.solvers.acc'%data.name, data.time, 'center right', xlim, None,\
			'%s.compare.solvers.tkde.acc'%data.name, data.time, 'best', xlim, None,\
			otherfunc)

