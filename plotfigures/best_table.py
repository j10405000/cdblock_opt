#!/usr/bin/env python
import sys,os
from data import *
solvers =['BLOCK-L-10', 'VW', 'AVG' ]
datasets = [leisure5, kdd40, web40, epsilon30]
datasets = [web40, epsilon30, kdd40 ]
#datasets = [heart_scale5]


if len(sys.argv) > 2:
	print('[Usage] ./best_table.py [logdir]')
	exit(1)
elif len(sys.argv) == 2:
	logdir = sys.argv[1]
else:
	logdir = '../log'

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

		primal, accuracy, iters = {}, {}, {}
		liblinear_loadtime = 0
		for line in open(acclog):
			line = line.strip()
			if line == '' or line[0] == '$' or 'iter' not in line or 'accuracy' not in line:
				#print 'skip %s' %line
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

		# shift initial data loading/preprocessing time
		timeshift = 0
		if solver.startswith('BLOCK'):  timeshift = data.time
		elif solver.startswith('AVG'):  timeshift = data.time
		elif solver.startswith('VW'): timeshift = data.vwtime
		elif solver.startswith('LIBLINEAR'): timeshift = liblinear_loadtime
		times[solver] = [t+timeshift for t in times[solver]]
	for solver in solvers:
		#accuracys[solver] = [abs((acc-bestacc)/bestacc) for acc in accuracys[solver]]
		accuracys[solver] = [100*acc for acc in accuracys[solver]]
	return times,  accuracys

for solver in solvers:
	print solver+"-1",
	for data in datasets:
		times, accuracys = getcoordinates(data)
		print " & %.2f & %d "%(accuracys[solver][0],times[solver][0]),
	print "\\\\"
	if solver == 'AVG':
		continue
	print solver+"-10",
	for data in datasets:
		times, accuracys = getcoordinates(data)
		print " & %.2f & %d "%(accuracys[solver][9],times[solver][9]),
	print "\\\\"
