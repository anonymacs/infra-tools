#!/usr/bin/env python
# -*- coding: utf-8 -*-#

import os, commands


#==========================
# 初期設定値 
#==========================

#=== BASIC認証 ===#
#b_id = "user"
#b_pass = "pass-phrase"

#=== POST認証 ===#
id = 'foo@bar'			# id
pp = 'password'			# pass
form_id = "login_id"	# form ID
form_pp = "login_pass"	# form Pass


#=== URL ===#
loginurl = 'https://www.xxx.zz/login.php'		# ログインフォームURL
geturl = 'https://www.xxx.zz/user/main.php'		# ログイン後のURL

#=== tmpファイル ===#
cookie = "/tmp/cookie.tmp"	# クッキー用ファイル
tmpfile = "ipass.txt"		# tmpファイル


#==========================
# メイン処理
#==========================

#com_login = 'wget -q -O - --save-cookies='+ cookie +' --keep-session-cookies --http-user='+ b_id +' --http-passwd='+ b_pass +' --post-data "'+ p_id_name +'='+ p_id +'&'+ p_pass_name +'='+ p_pass +'" '+ loginurl
com_login  = 'wget -q -O - --post-file='+ tmpfile +' --save-cookies='+ cookie +' --keep-session-cookies '+ loginurl
#com_get   = 'wget -q -O - --load-cookies='+ cookie +' --http-user='+ b_id +' --http-passwd='+ b_pass +' '+ geturl
com_get    = 'wget -q -O - --load-cookies='+ cookie +' '+ geturl

commands.getoutput(com_login)
status = commands.getoutput(com_get)
print status

os.remove(cookie)
#os.remove(tmpfile)
