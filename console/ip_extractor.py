#!/usr/bin/env python
# -*- coding: utf-8 -*-#
import os, commands


#==========================
# 初期設定値
#==========================

output  = 'ipaddrs.txt'

dir     = '/'

ex_ips  = [
			 '[0-9]\{4\}'	# 4-digit number
			,'127.0.0.1'
			,'192.168.0.'
]

ex_dirs = [
			 '/boot'
			,'/tmp'
			,'/root'
			,'/proc'
			,'/var/spool'
			,'/var/run'
			,'/etc/pki'
			,'/lib/modules'
			,'/usr/lib'
			,'/usr/share'
			,'/src'
			,'*/log'
			,'*log/*'
			,'*.dump'
]



#==========================
# メイン処理
#==========================

# 除外ディレクトリの整形
for i in range(len(ex_dirs)):
	ex_dirs[i] = '-path '+ ex_dirs[i].replace('/', '\/') + ' -prune'
ex_dirs = " -or ".join(ex_dirs)

# 除外IPアドレスの整形
for i in range(len(ex_ips)):
	ex_ips[i] = "grep -v '"+ ex_ips[i].replace('.', '\.') +"'"
ex_ips = "|".join(ex_ips)

# 抽出する IPv4 のマッチ式
ipv4     = "'[1-2]\?[0-9][0-9]\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'"
#ipv4d3   = "'[1-2][0-9][0-9]\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'"	// 先頭3桁のIPのみ
#ipv4d2   = "'[1-9][0-9]\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'"					// 先頭2桁のIPのみ


com = 'find '+ dir +' \( '+ ex_dirs +' \) -o -type f -print0 | xargs -0 grep -e ' + ipv4 +'|'+ ex_ips +' > '+ output

print com

commands.getoutput(com)
