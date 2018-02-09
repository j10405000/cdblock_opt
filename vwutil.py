#!/usr/bin/env python

import os, sys
from commands import getoutput

vwbin = 'vw/vw-5.1/vw'

def execmd(cmd):
	print(cmd)
	if  os.path.exists('dropcache'):
		cmd = './dropcache;' + cmd
	return getoutput(cmd)

def gen_vwcache(datasrc, datacache):
	cmd ="%s -d %s --cache_file %s --noop -b 24  -l 1000 --compressed --loss_function hinge " % (vwbin, datasrc, datacache) 
	if not os.path.exists(datacache):
		execmd(cmd)

def vwtrain(datacache, model, old_model=""):
	cmd = "/usr/bin/time -p %s --cache_file %s -f %s --passes 1 -b 24 --compressed --loss_function hinge " % (vwbin, datacache, model)
	if old_model: 
		cmd += " -i %s" % old_model
	time = execmd(cmd).split('\n')[-3].split()[-1]
	return float(time)
	
def vwpredict(datacache, model, output, labels):
	cmd = "%s -t --cache_file %s -i %s --compressed -b 24 -p %s" % (vwbin, datacache, model, output)
	execmd(cmd)
	predlabels = open(output)
	truelabels = open(labels)
	correct, total = 0, 0
	for pred, label in zip(predlabels, truelabels):
		total +=1
		if float(pred.strip()) * float(label.strip()) >= 0:
			correct += 1
	return float(correct)/total

def vwitertrain(datacache, datacache_t, labels, log, maxiters=50):
	old_model, new_model  = 'models/old.vwmodel', 'models/new.vwmodel'
	log = open(log,'w')
	total_time = 0
	iter = 1
	while iter <= maxiters:
		if iter == 1:
			time = vwtrain(datacache, new_model)
		else:
			time = vwtrain(datacache, new_model, old_model)
		total_time += float(time)
		acc = vwpredict(datacache_t, new_model, 'models/vwpredict.out', labels)
		log.write("iter %s time %s accuracy %.6f\n" % (iter, total_time, acc))
		execmd('mv %s %s' % (new_model, old_model))
		iter += 1

if __name__ == '__main__':
	#Check the existence of trainer
	if not os.path.exists(blocktrain):
		os.system('cd cdblock;make')
	#Check the existence of log dir
	if not os.path.exists('log/time'):
		os.system('mkdir -p log/time')

	for data in datasets:
		logname = 'log/time/%s#%s' % (data.name, 'VW')
		if os.path.exists(logname):
			print 'Already ran this.. skip it'
			continue
		else:
			logtmp = logname + '.tmp'

		traincache = 'data/%s.vwcache' % data.train
		testcache = 'data/%s.vwcache' % data.test
		testlabel = 'data/%s.test+'.label

		vwitertrain(traincache, testcache, testlabel, logtmp, 250)
		execmd('mv %s %s' % (logtmp, logname))
		execmd('cp %s log/acc/%s#%s.acc' % (data.name, 'VW'))


#vwtrain(sys.argv[1], sys.argv[2])
#vwitertrain(sys.argv[1],sys.argv[2],sys.argv[3])
#print vwpredict(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


