#!/usr/bin/env python

import sys, os
from commands import getoutput
from data import *

blocktrain = './cdblock/blocktrain'
liblineartrain = './liblinear/train'
streamtrain = './streamsvm/streamtrain'
streampredict = './streamsvm/predict'

datasets = [web40, epsilon30, kdd40, leisure5]
datasets = [web40, epsilon30, kdd40]
#datasets = [heart_scale5]
solvers = ['BLOCK-L-D','BLOCK-L-1','BLOCK-L-10','BLOCK-L-20', \
		'BLOCK-P-B', 'BLOCK-P-I'] #, 'LIBLINEAR', 'STREAMSVM']

#measure time or acc
if len(sys.argv) != 2 or sys.argv[1] not in ['acc','time']:
	print('[Usage] ./go-compare-solvers-tkdd.py time|acc')
	exit(1)

if sys.argv[1] == 'time':
	acc = 0
elif sys.argv[1] == 'acc':
	acc = 1

#Check the existence of trainers
for trainer in [blocktrain, liblineartrain, streamtrain]:
	if not os.path.exists(trainer):
		os.system('cd cdblock;make')
		os.system('cd liblinear;make')
		os.system('cd streamsvm;make')
#Check the existence of log dirs
if not os.path.exists('log/time') or not os.path.exists('log/acc'):
	os.system('mkdir -p log/time')
	os.system('mkdir -p log/acc')

def execmd(cmd):
	if not acc and os.path.exists('dropcache'):
		cmd = './dropcache;' + cmd
	print '  $ %s' % (cmd)
	getoutput(cmd)

for data in datasets:
	for s in solvers:
		if acc: 
			logname = 'log/acc/%s#%s.acc' % (data.name, s)
		else: 
			logname = 'log/time/%s#%s' % (data.name, s)
		print 'Generate "%s"' % logname
		if os.path.exists(logname):
			print 'Already ran this.. skip it'
			continue
		else:
			logtmp = logname + '.tmp'

		BLOCK_options = '%s -e 0.0001 -B -1 -c 1 -m 30 -p' % blocktrain

		if s == 'BLOCK-L-D':
			if not acc:
				execmd('%s -s 3 data/%s.%s | tee %s' % \
						(BLOCK_options, data.train, data.blocks, logtmp))
			else :
				execmd('%s -s 3 -S %s -o -t data/%s.cbin data/%s.cbin | tee %s' % \
						(BLOCK_options, data.blocks, data.test, data.train, logtmp))
		elif s == 'BLOCK-L-1':
			if not acc:
				execmd('%s -s 3 -M 1 data/%s.%s | tee %s' % \
						(BLOCK_options, data.train, data.blocks, logtmp))
			else :
				execmd('%s -s 3 -M 1 -S %s -o -t data/%s.cbin data/%s.cbin | tee %s' % \
						(BLOCK_options, data.blocks, data.test, data.train, logtmp))
		elif s == 'BLOCK-L-5':
			if not acc:
				execmd('%s -s 3 -M 5 data/%s.%s | tee %s' % \
						(BLOCK_options, data.train, data.blocks, logtmp))
			else :
				execmd('%s -s 3 -M 5 -S %s -o -t data/%s.cbin data/%s.cbin | tee %s' % \
						(BLOCK_options, data.blocks, data.test, data.train, logtmp))
		elif s == 'BLOCK-L-10':
			if not acc:
				execmd('%s -s 3 -M 10 data/%s.%s | tee %s' % \
						(BLOCK_options, data.train, data.blocks, logtmp))
			else :
				execmd('%s -s 3 -M 10 -S %s -o -t data/%s.cbin data/%s.cbin | tee %s' % \
						(BLOCK_options, data.blocks, data.test, data.train, logtmp))
		elif s == 'BLOCK-L-15':
			if not acc:
				execmd('%s -s 3 -M 15 data/%s.%s | tee %s' % \
						(BLOCK_options, data.train, data.blocks, logtmp))
			else :
				execmd('%s -s 3 -M 15 -S %s -o -t data/%s.cbin data/%s.cbin | tee %s' % \
						(BLOCK_options, data.blocks, data.test, data.train, logtmp))
		elif s == 'BLOCK-L-20':
			if not acc:
				execmd('%s -s 3 -M 20 data/%s.%s | tee %s' % \
						(BLOCK_options, data.train, data.blocks, logtmp))
			else :
				execmd('%s -s 3 -M 20 -S %s -o -t data/%s.cbin data/%s.cbin | tee %s' % \
						(BLOCK_options, data.blocks, data.test, data.train, logtmp))
		elif s == 'BLOCK-P-B':
			if not acc:
				execmd('%s -s 7 data/%s.%s | tee %s' % \
						(BLOCK_options, data.train, data.blocks, logtmp))
			else :
				execmd('%s -s 7 -S %s -o -t data/%s.cbin data/%s.cbin | tee %s' % \
						(BLOCK_options, data.blocks, data.test, data.train, logtmp))
		elif s == 'BLOCK-P-I':
			if not acc:
				execmd('%s -s 8 data/%s.%s | tee %s' % \
						(BLOCK_options, data.train, data.blocks, logtmp))
			else :
				execmd('%s -s 8 -S %s -o -t data/%s.cbin data/%s.cbin | tee %s' % \
						(BLOCK_options, data.blocks, data.test, data.train, logtmp))
		elif s == 'LIBLINEAR':
			iter = 10
			if data.name in ['web40','epsilon30']: iter = 2
			if not acc:
				execmd('%s -s 3 -c 1 -m %s -e 0.0001 data/%s | tee %s' % \
						(liblineartrain, iter, data.train, logtmp))
			else :
				execmd('%s -s 3 -c 1 -m 50 -e 0.0001 -o -b -t data/%s.cbin data/%s.cbin | tee %s' % \
						(liblineartrain, data.test, data.train, logtmp))
		elif s == 'STREAMSVM':
			if not acc:
				execmd('%s -c 1 data/%s models/%s_stream.model | tee %s' % \
						(streamtrain, data.train, data.train, logtmp))
			else :
				execmd('%s -c 1 data/%s models/%s_stream.model ' % \
						(streamtrain, data.train, data.train))
				execmd('%s data/%s models/%s_stream.model /dev/null | tee %s' % \
						(streampredict, data.test, data.train, logtmp))
		else :
			print 'Wrong Solvers'

		# change log name to the correct one
		execmd('mv %s %s' % (logtmp, logname))

