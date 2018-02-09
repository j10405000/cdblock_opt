#!/usr/bin/env python

import sys, os
from commands import getoutput
from data import *

blocktrain = './cdblock/blocktrain'

#datasets = [heart_scale, epsilon]
datasets = [heart_scale5, heart_scale10, heart_scale20]
datasets = [web40, web200, web400, web1000]

#Check the existence of trainer
if not os.path.exists(blocktrain):
	os.system('cd cdblock;make')
#Check the existence of log dir
if not os.path.exists('log/time'):
	os.system('mkdir -p log/time')

def execmd(cmd):
	if  os.path.exists('dropcache'):
		cmd = './dropcache;' + cmd
	print '  $ %s' % (cmd)
	getoutput(cmd)

for data in datasets:
	logname = 'log/time/%s#%s' % (data.name, 'BLOCK-L-D')
	print 'Generate "%s"' % logname
	if os.path.exists(logname):
		print 'Already ran this.. skip it'
		continue
	else:
		logtmp = logname + '.tmp'
	execmd('%s -s 3 -e 0.0001 -B -1 -c 1 -m 15 -p data/%s.%s | tee %s' %\
			(blocktrain, data.train, data.blocks, logtmp))

	# change log name to the correct one
	execmd('mv %s %s' % (logtmp, logname))

