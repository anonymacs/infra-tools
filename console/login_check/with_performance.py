#!/usr/bin/env python
# -*- coding: utf-8 -*-#
# set tabstop:4

import sys
import time
import datetime
import GetURL
import SMMailer


# UTF-8用の初期化
reload(sys)
sys.setdefaultencoding('utf-8')

#================================================================
# 初期設定値 
#================================================================

params = [
	 {
		 'domain'	: 'xxx.com'
		,'scheme'	: 'https://'
		,'lg_path'	: '/login/monitoring_index.php'
		,'gt_path'  : '/logined/monitoring_index.php'
		,'queries'	: {
						 'mode'					: 'login'
						,'login_mo_pc_mail'		: 'hoge'		#// id
						,'login_mo_password'	: 'fuga'					#// pp
					}
	}
#	,{}
]


#================================================================
# メイン処理 クラス記述
#================================================================

class Checker:

	#/**
	# * 初期設定値を記入する
	# * アドレス・遅延判定
	# * @param	-
	# * @author	2011.10.13 takuma.m
	# * @return	-
	# */
	def __config (self):
		# メール送信用
		self.from_addr = 'info@xxx.com'
		self.to_addr = 'hoge@hoge.com'

		# $slow秒以上ならメール送信
		self.slow = 2
		self.header = '日付： '
		self.footer = ''


	#/**
	# * コンストラクタ
	# * @param	list params URL・ログインID等のパラメーター
	# * @author	2011.10.13 takuma.m
	# * @return	-
	# */
	def __init__ (self,params) :
		self.mail_flg = 0
		self.params = params
		self.__config()


	#/**
	# * メイン処理 ログイン試行後、遅延判定を行う
	# * @param	-
	# * @author	2011.10.13 takuma.m
	# * @return	-
	# */
	def main(self):
		body = ''
		
		for p in self.params :
			uri = p['scheme'] + p['domain']
		#	print "Start to get the data from " + uri
			# 接続用インスタンス作成
			res = GetURL.GetURL(uri,self)
			# POSTクエリの作成
			res.makeQuery(p['queries'])

			resp = []
			# login処理
			resp.append( res.login(p['lg_path']) )
			# login後の表示処理
			resp.append( res.getResp(p['gt_path']) )

			# 速度判定
			body += self.check(resp)
			
		if self.mail_flg != 0 :
			self.mail()
		
		dt = datetime.datetime.today()
		dt = dt.strftime("%x %X")
		print dt
		for logger in resp:
			print logger

	#/**
	# * 遅延判定処理
	# * @param	list resp レスポンス数値
	# * @author	2011.10.13 takuma.m
	# * @return	T:メール送信用の文 F:空文
	# */
	def check(self, resp):
		body = ''
		
		# レスポンス（ベンチ結果）の数値変換
		for i in range(len(resp)):
			resp[i] = resp[i].split("\n")[1]

			if float(resp[i]) > self.slow :
				self.mail_flg = 1
				msg = self.uri + '- 第'+ i +'ステップに'+ str(self.slow) +'秒以上かかりました'
				msg = msg + "\n->" +  str(resp1) +'秒'
				body = body + msg + "\n"
		
		return body


	#/**
	# * メール送信処理
	# * @param	str body メール本文
	# * @author	2011.10.13 takuma.m
	# * @return	T: True
	# */
	def mail(self, body):
		
		# メール本文用日付
		dt = datetime.datetime.today()
		dt = dt.strftime("%x %X")

		subj   = '[Notice] Slow Performance'
		header = self.header + dt + "\n\n"
		body   = header + "\n".join(body) + self.footer
		ml = SMMailer.SMMailer(self.from_addr, self.to_addr, subj, body )
		return True

	
	def err(self,msg,uri):
		print msg

		# メール本文用日付
		dt = datetime.datetime.today()
		dt = dt.strftime("%x %X")
		
		subj   = '[Alert] Slow Performance Error'
		header = self.header + dt + "\n\n"
		header += '対象ドメイン: ' + uri + "\n"
		body   = header + msg + self.footer
		ml = SMMailer.SMMailer(self.from_addr, self.to_addr, subj, body )
		
		sys.exit(1)

#================================================================
# メイン処理
#================================================================

if __name__ == '__main__':
	check = Checker(params)
	check.main()


