#!/usr/bin/env python
# -*- coding: utf-8 -*-#

import cookielib, urllib2, re


class GetURL:
	
	def __init__ (self, uri, get_path, tk_path=''):
		self.uri = uri
		self.get_path = get_path
		self.tk_path = tk_path
	
	def getToken(self, id, pp, id_post, tk_str):
		req = urllib2.Request(self.uri + self.tk_path, id_post % (id, pp))
		self.opener = urllib2.build_opener()
		self.opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
		conn = self.opener.open(req)
		cont = conn.read()
		token =  re.search(tk_str, cont).group(1)
		return token
	
	def login (self):
		pass
	
	def getResp (self, tk_post, token):
		req = urllib2.Request(self.uri + self.get_path , tk_post % (token))
		conn = self.opener.open(req)
		cont = conn.read()
		return cont

