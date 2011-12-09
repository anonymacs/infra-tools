#!/usr/bin/env python
# -*- coding: utf-8 -*-#

import os

class TPL:

	def __init__(self, params):
		path = os.path.dirname(__file__)
		self.file = path + '/mail.tpl'
		self.params = params
	
	def getConv(self):
		data = self.read()
		body = self.tmpl(data)
		return body
	
	def read(self):
		f = open(self.file)
		data = f.read()
		f.close()
		return data
	
	def tmpl(self, data):
		body = data % self.params
		return body

