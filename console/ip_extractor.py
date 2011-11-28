#!/usr/bin/env python
# -*- coding: utf-8 -*-#
import os, commands


#==========================
# �����ݒ�l
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
# ���C������
#==========================

# ���O�f�B���N�g���̐��`
for i in range(len(ex_dirs)):
	ex_dirs[i] = '-path '+ ex_dirs[i].replace('/', '\/') + ' -prune'
ex_dirs = " -or ".join(ex_dirs)

# ���OIP�A�h���X�̐��`
for i in range(len(ex_ips)):
	ex_ips[i] = "grep -v '"+ ex_ips[i].replace('.', '\.') +"'"
ex_ips = "|".join(ex_ips)

# ���o���� IPv4 �̃}�b�`��
ipv4     = "'[1-2]\?[0-9][0-9]\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'"
#ipv4d3   = "'[1-2][0-9][0-9]\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'"	// �擪3����IP�̂�
#ipv4d2   = "'[1-9][0-9]\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'"					// �擪2����IP�̂�


com = 'find '+ dir +' \( '+ ex_dirs +' \) -o -type f -print0 | xargs -0 grep -e ' + ipv4 +'|'+ ex_ips +' > '+ output

print com

commands.getoutput(com)
