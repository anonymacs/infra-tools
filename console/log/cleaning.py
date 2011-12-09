#!/usr/bin/env python
# -*- encoding: utf-8 -*- 

import sys
import datetime

#=== === === === ===
# Initial Parameters
#=== === === === ===
dt_crit = 90




#=== === === === ===
# Define Functions
#=== === === === ===
def getDate(dt):
	dt  = dt.split(' ')
	ymd = dt[0].split('/')
	hms = dt[1].split(':')

	dt = datetime.datetime( int(ymd[0]), int(ymd[1]), int(ymd[2]), int(hms[0]), int(hms[1]) ,int(hms[2]) )
	return dt



# === === === === ===
# Main Process
# === === === === ===

#== read file
#f = open('./dp_sb.txt')
#f = open('./dp_au.txt')
#f = open('./dp_docomo.txt')
f = open('./prev2_docomo.txt')
f_data = f.read()

lines = f_data.split('\n')
if False is bool(lines[-1]):
	lines.pop()


#== loop file lines 
list = []
for line in lines:
	
	col = line.split(',')
	#= get UserAgent
	ua  = col[2]
	#= get time
	dt  = getDate(col[1])

	#= check the list either empty or not
	if False is bool(list):
		list.append( {'date' : dt, 'ua' : ua} )
		print line
	else:
		#= set date for check
		chk_dt = dt - datetime.timedelta(minutes=dt_crit)
		#= sort list with asc order
		list.sort(lambda a, b: cmp(a['date'], b['date']))

		#= loop the list for checking the past date
		flg_del = False
		for i in range(len(list)):
			if  chk_dt < list[i]['date']:
				break
			else:
				flg_del = True
		#= delete the past date from the list
		if flg_del is True:
			del list[0:i+1]

		#= loop the list for checking the duplicated User-Agent
		flg_dup = False
		for val in list:
			if val['ua'] == ua:
				flg_dup = True
				break

		
		if flg_dup is False:
			list.append( {'date' : dt, 'ua' : ua} )
			print line

print 'END'
