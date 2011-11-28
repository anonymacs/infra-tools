#!/usr/bin/env python
# -*- coding: utf-8 -*-#
#########################################
### Ping to SubNet
#########################################

import os, commands, sys


### $cIP[op0]=$num[op1]=$sec[op2]=$out[op3] ###
ip = sys.argv

if (len(ip) != 2):
	print "arg error"
	
else:
	op = ip[1].split('=')
	ip = commands.getoutput('ping -c'+ op[1] +' -i'+ op[2] +' -w'+ op[3] +' '+ op[0])
	ip = ip.split('\n')
	ip = ip[-2].split(' ')
	if int(ip[3]) == int(op[1]):
		print '○'
	elif 0 < int(ip[3]) and int(ip[3]) < int(op[1]):
		print '△'
	elif int(ip[3]) == 0:
		print '×'
	else:
		print 'error'
