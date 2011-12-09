#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate


class SMMailer:

	def __init__(self, from_addr, to_addr, subj, body ):
		self.from_addr = from_addr
		self.to_addr = to_addr
		self.subj = subj
		self.body = body
		self.enc = 'ISO-2022-JP'
		self.main()
	
	def main(self):
		msg = self.create()
		self.send(msg)

	def create(self):
		# msg = MIMEText(body, 'plain', encoding)
		msg = MIMEText(self.body.encode(self.enc), 'plain', self.enc)
		msg['Subject'] = Header(self.subj, self.enc)
		msg['From'] = self.from_addr
		msg['To'] = self.to_addr
		msg['Date'] = formatdate()
		return msg

	def send(self, msg):
		s = smtplib.SMTP('localhost', 25)
		s.sendmail(self.from_addr, [self.to_addr], msg.as_string())
		s.close()

