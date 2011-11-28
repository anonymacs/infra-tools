#!/usr/bin/env python
# -*- coding: utf-8 -*-#

import cookielib, urllib, urllib2


#========================
# 初期設定値 
#========================

id       = 'foo@bar.zz'		# ログインID
pp       = 'pass-phrase'	# ログインパスワード
form_id  = 'login_id'		# id (form パラメータ)
form_pp  = 'login_pass'		# pass (form パラメータ)

# ログインページURL （フォーム内容をPOSTする先）
loginurl = 'https://www.xxx.zz/login.php'
# ログイン後のURL
geturl   = 'https://www.xxx.zz/user/main.php'



#========================
# メイン処理
#========================

# セッション保持用のヘッダー
headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'Connection': 'keep-alive',
        "Accept": "text/plain"
}

# <form>パラメーターを指定
postdata = {}
postdata[form_id] = id
postdata[form_pp] = pp
params = urllib.urlencode(postdata)


# POSTでアクセス
req = urllib2.Request(loginurl, params, headers)
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.open(req).read()

check = urllib2.Request(geturl)
response = opener.open(check).read()
print response
