#!/usr/bin/env python
# -*- coding: utf-8 -*-#

#########################################
### ver 3.0 Britain
#########################################

import os, commands, re, sys


#================================================================
# 初期設定値 
#================================================================
## Applogicフラグ
applogic = 1

## 実行ディレクトリ
basedir = '/var/serverinfo'

## 送信先IPアドレスとユーザー
sendip = '127.0.0.1'
senduser = 'filescp'

sendto = senduser +'@'+ sendip

## 宛先ディレクトリ
senddir = '/var/www/html/serverinfo/'

## SCP接続用の鍵の場所
sshkey = basedir +'/.ssh/id_rsa'

keyuser=''

## 初期化
complexdata = ""
ipaddr = ""

user1 = ''
user2 = ''

#================================================================
# 初回実行処理
#================================================================
if not os.path.exists(sshkey) :
	print '初回起動: sshkeyを作成します'
	commands.getoutput('mkdir ' + basedir +'/.ssh/')
	print 'scp '+ sendto +':/home/filescp/.ssh/id_rsa ' + basedir +'/.ssh/' +'\t'
	commands.getoutput('scp '+ sendto +':/home/filescp/.ssh/id_rsa ' + basedir +'/.ssh/')
#	commands.getoutput('scp '+ sendto +' "cat /home/'+ senduser +'/.ssh/id_rsa" | cat >> '+ sshkey)
	if keyuser == '':
		if os.path.exists('/home/' + user2 + '/.ssh/id_rsa') :
			keyuser = user2 +'.'+ user2
		else:
			keyuser = user1 +'.'+ user1
	else:
		keyuser = keyuser +'.'+ keyuser
	
	commands.getoutput('chown '+ keyuser +' '+ sshkey)
#	commands.getoutput('scp -i '+ sshkey +' '+ sendto +':/home/filescp/serverinfo.py ' + basedir)

	if not os.path.exists(sshkey):
		print 'sshkey作成に失敗しました。終了します。'
		sys.exit()
	else:
		print 'sshkeyを作成しました。もう一度起動してください。'
		sys.exit()
elif os.path.getsize(sshkey) == 0:
	print 'ssh '+ sendto +' "cat /home/'+ senduser +'/.ssh/id_rsa" | cat >> '+ sshkey +'\n'
	commands.getoutput('ssh '+ sendto +' "cat /home/'+ senduser +'/.ssh/id_rsa" | cat >> '+ sshkey)
else:
	print "最新版を使うためには\n"+ 'scp -i '+ sshkey +' '+ sendto +':/home/filescp/serverinfo.py ' + basedir + "を実行してください"

#================================================================
# IPとホスト名を取得
#================================================================
## Applogic用の設定ファイルからIP情報を取得
if applogic == 1 and os.path.exists('/etc/applogic/appliance.conf') :
	print "Applogic情報を取得します\n"
	f = open('/etc/applogic/appliance.conf', 'r')
	appdatas = f.readlines()
	f.close()
	for line in appdatas :
		line = line.split('=')
		if line[0] == 'primary_ip' :
			## IP設定ファイル(ifcfg-eth)からIPアドレスを取得
			ipaddr = ""
			eth = commands.getoutput('locate /etc/sysconfig/network-scripts/ifcfg-eth0')
			eth = eth.split('\n')
			for val in eth:
				f = open(val, 'r')
				ethdatas = f.readlines()
				f.close()
				for line in ethdatas :
					line = line.split('=')
					if line[0] == 'IPADDR' :
						ipaddr += line[1].rstrip("\n") +'<br />'
			ipaddr.rstrip('<br />')
		elif line[0] == '_APP_NAME' :
			## アプリケーション名を取得
			appname = f_appname = line[1].rstrip("\n")
		elif line[0] == '_COMP_CLASS' :
			aplance = line[1].rstrip("\n")
## Applogic設定ファイルを使わない場合
else:
	print "サーバー名（uname）を取得します\n"
	## サーバー名を取得
	uname = os.uname()	
	f = open('/etc/sysconfig/network-scripts/ifcfg-eth0', 'r')
	appdatas = f.readlines()
	f.close()
	for line in appdatas :
		line = line.split('=')
		if line[0] == 'IPADDR' :
			## IPアドレスを取得
			ipaddr = line[1].rstrip("\n")
	appname = f_appname = uname[1]

## Applogicの複雑なアプリの場合の処理
if ipaddr == "":
	print "外部スクリプトからIPアドレスを取得します\n"	
	complexdata = commands.getoutput('wget -q -O - http://'+ sendip +'/dirsize/ipaddr.php')
	complexdata = complexdata.split('=')
	ipaddr = complexdata[0]
	f_appname =  appname + '_'+ aplance[1:]
	print "IPアドレス：" + ipaddr + "\nアプリ名："+ f_appname +"\n"


## 保存ファイル名を代入
file = f_appname + '.txt'


#================================================================
# サーバー情報の取得
#================================================================

print '"df -h"を実行中...'
hdddata = commands.getoutput('df -h')
hdddata = hdddata.split('\n')
hdddata.pop(0)
hdd = []
nas = 0
for line in hdddata :
	line = re.split("\s+", line)
	if line[0].startswith("nfs:"):
		print "NASを検出しました"
		nas = 1
		nashdd = line[1] +'\t'+ line[2] +'\t'+ line[4] +'\t'+ line[3]
	elif line[0].startswith("/dev/"):
		print "HDDを検出しました"
		hdd = line[1] +'\t'+ line[2] +'\t'+ line[4] +'\t'+ line[3]

print 'CPU情報を取得中...'
cpudata = commands.getoutput('cat /proc/cpuinfo | grep processor')
cpudata = cpudata.split("\n")
cpu = str(len(cpudata))
memdata = commands.getoutput('cat /proc/meminfo  | grep ^MemTotal')
memdata = re.split("\s+", memdata)
memtotal = str(int(memdata[1]) / 1024) + 'MB'
memdata = commands.getoutput('cat /proc/meminfo  | grep ^MemFree')
memdata = re.split("\s+", memdata)
memfree = int(memdata[1]) / 1024
memdata = commands.getoutput('cat /proc/meminfo  | grep ^Buffers')
memdata = re.split("\s+", memdata)
membuf = int(memdata[1]) / 1024
memdata = commands.getoutput('cat /proc/meminfo  | grep ^Cached')
memdata = re.split("\s+", memdata)
memcache = int(memdata[1]) / 1024

## メモリー情報を文字列へ整形
memfree2 = str(memfree + memcache + membuf) + 'MB'
memfree = str(memfree) + 'MB'
membuf = str(membuf) + 'MB'
memcache = str(memcache) + 'MB'



#================================================================
# バージョンの確認
#================================================================
## 初期化
version = []

## ミドルウェア洗い出し用
versions = {}

## [0] apacheのバージョン確認
try:
	tmp = commands.getoutput('/usr/local/apache2/bin/httpd -v 2> /dev/null | grep version')
	tmp = re.split("\s+", tmp)
	version.append( tmp[2].lstrip('Apache/') )
	versions["apache"] = tmp[2].lstrip('Apache/')
	
except:
	version.append( '-' )
	versions["apache"] = 

## [1] apache (yum)のバージョン確認
try:
	tmp = commands.getoutput('/usr/sbin/httpd -v 2> /dev/null')
	tmp = re.split("\s+", tmp)
	tmp = tmp[2]
	version.append( tmp.lstrip('Apache/') )
except:
	version.append( '-' )

## [2] PHPのバージョン確認
try:
	tmp = commands.getoutput('/usr/local/bin/php -v 2> /dev/null | grep cli')
	tmp = re.split("\s+", tmp)
	version.append( tmp[1] )
except:
	version.append( '-' )

## [3] eAcceleratorのバージョン確認
try:
	tmp = commands.getoutput('/usr/local/bin/php -v 2> /dev/null | grep  eAccelerator')
	tmp = re.split("\s+", tmp)
	version.append( tmp[3].rstrip(',').lstrip('v') )
except:
	version.append( '-' )

## [4] PostgreSQLのバージョン確認
try:
	tmp = commands.getoutput('/usr/local/pgsql/bin/psql --version 2> /dev/null | grep PostgreSQL')
	tmp = re.split("\s+", tmp)
	version.append( tmp[2] )
except:
	version.append( '-' )

## [5] MySQLのバージョン確認
try:
	tmp = commands.getoutput('/usr/bin/mysql --version 2> /dev/null')
	tmp = re.split("\s+", tmp)
	version.append( tmp[4].rstrip(',') )
except:
	version.append( '-' )

## [6] zabbix-agentのバージョン確認
try:
	tmp = commands.getoutput('/usr/sbin/zabbix_agent --version 2> /dev/null | grep Zabbix')
	tmp = re.split("\s+", tmp)
	version.append( tmp[2].lstrip('v') )
except:
	version.append( '-' )



#================================================================
# 起動項目の確認 (Runレベル3)
#================================================================
autoruns = commands.getoutput('/sbin/chkconfig --list | grep 3:on')
autoruns = autoruns.split("\n")
tmp = {}

for line in autoruns :
	line = re.split("\s+", line)
## 自動起動しているアプリの確認
	if line[0].startswith("apache"):
		tmp['apache'] = 1
	elif line[0].startswith("httpd"):
		tmp['httpd'] = 1
	elif line[0].startswith("pgsql"):
		tmp['pgsql'] = 1
	elif line[0].startswith("postgresql"):
		tmp['pgsql'] = 1
	elif line[0].startswith("mysqld"):
		tmp['mysql'] = 1
	elif line[0].startswith("vsftpd"):
		tmp['vsftpd'] = 1
	elif line[0].startswith("zabbix-agent"):
		tmp['zabbix'] = 1

autorun = []

try:
	if tmp['apache'] == 1:
		autorun.append('○')
except:
	if version[0] == '-':
		autorun.append('-')
	else:
		autorun.append('×')
try:
	if tmp['httpd'] == 1:
		autorun.append('○')
except:
	if version[1] == '-':
		autorun.append('-')
	else:
		autorun.append('×')
try:
	if tmp['pgsql'] == 1:
		autorun.append('○')
except:
	if version[4] == '-':
		autorun.append('-')
	else:
		autorun.append('×')
try:
	if tmp['mysql'] == 1:
		autorun.append('○')
except:
	if version[5] == '-':
		autorun.append('-')
	else:
		autorun.append('×')
try:
	if tmp['vsftpd'] == 1:
		autorun.append('○')
except:
	autorun.append('×')
try:
	if tmp['zabbix'] == 1:
		autorun.append('○')
except:
	if version[6] == '-':
		autorun.append('-')
	else:
		autorun.append('×')


#================================================================
# 関数：HTMLファイル作成用関数
#================================================================
def htmloutput(data, file):

	print "書き込み準備中です\n"


	result= f_appname +'\t'+\
			ipaddr +'\t'+	\
			cpu +'\t'+		\
			memtotal +'\t'+	\
			memfree +'\t'+	\
			memfree2 +'\t'+	\
			data + "\n"
	
	for value in version:
		result += value + '\t'
	result = result.rstrip('\t') +'\n'
	
	for value in autorun:
		result += value + '\t'
	result = result.rstrip('\t')
	
	#---------------------- ファイルに出力 -----------------------#
	f = open( file, 'w')
	print file + "に書き込んでいます...\n"
	f.write(result)
	f.close()
	print file + "に書き込み完了しました\n"

	#---------------------- ファイルの転送 -----------------------#
	commands.getoutput('scp -i '+ sshkey +' ./'+ file +' '+send);
	print send +"へ送信完了しました\n"
	commands.getoutput('rm -f '+ file);




#================================================================
# プログラム処理の開始地点！
#================================================================

## SCP用の宛先作成 ##
send = sendto + ':' + senddir

## dataをHTMLに書き込み
htmloutput(hdd, file)


if nas == 1 :
	print "NAS用の処理を開始します\n"
	nasfile = appname + '_NAS.txt'
	f_appname = appname + '_NAS'
	ipaddr = cpu = memtotal = memfree = "-"
	num = 0
	while  len(version) > num:
		version[num] = '-'
		num += 1
	num = 0
	while  len(autorun) > num:
		autorun[num] = '-'
		num += 1
	htmloutput(nashdd, nasfile)


