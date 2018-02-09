#!/usr/bin/env python
import sys, os
from data import *
from commands import getoutput

datasets = [web40, epsilon30, leisure5, kdd40]
datasets = [web40, epsilon30, kdd40]
#datasets = [heart_scale5]
datadir = './'

vwbin = '../vw/vw-5.1/vw'

if not os.path.exists(vwbin):
	os.system('cd ../vw/vw-5.1; make; cd -')

def execmd(cmd):
	if os.path.exists('dropcache'):
		cmd = './dropcache;' + cmd
	print '  $ %s' % (cmd)
	return getoutput(cmd)

def genvwfmt(src):
	vwgen = "sed -e 's/^-1/-1 |features/' | sed -e 's/^+*1/1 |features/'"
	vwcache = "%s -d /dev/stdin --loss_function hinge --cache_file %s.vwcache --noop -b 24  -l 1000 --compressed" % (vwbin, src) 

	if os.path.exists('%s.vwcache' % src):
		print('\texists.')
		return None
	if not os.path.exists(src):
		print ('\tsource %s does not exist. Skip this data' % src)
	
	cmd = 'cat %s | %s | /usr/bin/time -p %s' % (src, vwgen, vwcache)
	time = execmd(cmd).split('\n')[-3].split()[-1]
	return time

#		os.system(cmd)
#	if isshuf == '1':
#		cmd = 'cat %s | %s | shuf - | %s' % (src, vwgen, vwcache)
#		print cmd
#		os.system(cmd)
#	else:
#		cmd = 'cat %s | %s | %s' % (src, vwgen, vwcache)
#		print cmd
#		os.system(cmd)

# for calculating accurcy of VW..
def getlabels(src, dest):
	if os.path.exists(dest):
		print('\texists.')
	cmd = "cut -d ' ' -f 1 %s > %s" % (src, dest)
	execmd(cmd)


if len(sys.argv) > 1:
	genvwfmt(sys.argv[1], sys.argv[2])
	exit(0)

for data in datasets:
	trainpath = os.path.join(datadir, data.train)
	testpath = os.path.join(datadir, data.test)
	testlabel = testpath+'.label'
	print('Generete VW format for %s ' % (data.name))
	isshuf = 0
	if data.name in ['kdd40', 'leisure5']:
		trainpath += '.shuf'
	
	time = genvwfmt(trainpath)
	if time:
		open('data.py','a').write('%s.vwtime = %s\n' % (data.name, time))
	genvwfmt(testpath)
	getlabels(testpath, testpath+'.label')


