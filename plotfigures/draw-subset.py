#!/usr/bin/env python
import sys, os
from data import *

datasets = [leisure5, web40, epsilon30, kdd40]
datasets = [web40, epsilon30, kdd40]

if len(sys.argv) > 2:
	print('[Usage] ./draw-subset.py [logdir]')
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
	block, acc,size= {}, {},{}
	for data in datasets:
		size[data], block[data], acc[data] = [], [], []
		acclog = os.path.join(logdir,'acc/%s#SUBSAMPLE_bestC.acc' % data.name)
		if not existlog(acclog):
			exit(1)
		print acclog		
		for line in open(acclog):
			line = line.strip()
			if line == '' or 'block' not in line:
				continue
			#print float(pt['accuracy'])
			pt = dict(zip(line.split()[::2],line.split()[1::2]))
			block[data] += [(float(pt['block'])+1)/data.blocks*100]
			acc[data] += [(float(pt['accuracy']))]
		bestacc= acc[data][-1]
		print bestacc
		acc[data] = [100*abs((a-bestacc)) for a in acc[data]]
	return block, acc,size

#Draw now!
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('text',usetex=True)
matplotlib.rc('font',family='serif',size='14')
matplotlib.rc(('xtick.major'), pad = 9)
from matplotlib import pylab

block, acc,size = getcoordinates()
pylab.figure()
params = {'axes.labelsize': 20, 'text.fontsize': 20, 'legend.fontsize': 20,'xtick.labelsize': 22,'ytick.labelsize': 22}
pylab.rcParams.update(params)
for i,data in enumerate(datasets):
	print data.name
	pylab.plot(block[data], acc[data], label='%s' % data.display, lw=3, c=mycolor(i), ls=mylinestyle(i))
	pylab.plot(block[data][1], acc[data][1],'o', ms=9,c=mycolor(i))
#pylab.xlim([2000,4000])
pylab.legend(loc='best')
pylab.xlabel('Percentage of the whole data set (\%)')
pylab.ylabel('Difference to the best accuracy (\%)')
if not os.path.exists('figures'):
	os.mkdir('figures')
for fmt in FILETYPE:
	pylab.savefig('figures/subsample.'+fmt)

pylab.figure()


#params = {'axes.labelsize': 20, 'text.fontsize': 20, 'legend.fontsize': 20,'xtick.labelsize': 22,'ytick.labelsize': 22}
#pylab.rcParams.update(params)
#print block
#print acc
#for i,data in enumerate(datasets):
#	print data.name
#	print block
#	print acc
#	pylab.plot(size[data], acc[data], label='%s' % data.display, lw=3, c=mycolor(i), ls=mylinestyle(i))
##pylab.xlim([2000,4000])
#pylab.legend(loc='best')
#pylab.xlabel('Data size (MB)')
#pylab.ylabel('Difference to the best accuracy (\%)')
#if not os.path.exists('figures'):
#	os.mkdir('figures')
#for fmt in FILETYPE:
#	pylab.savefig('figures/subsample_ijcai_size.'+fmt)
#

