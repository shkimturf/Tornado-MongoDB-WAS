# -*- coding: utf-8 -*-
'''
Created on 2016. 5. 26.

@author: Sunhong Kim
'''

from server.handlers import CommonHandler, authenticated_api

from app.error import HDError
from models.account.user import HDUser
from models.account.session import HDSession
from models.orm import HDORMObject

import tornado, utils, pymongo

class SignUpAPIHandler(CommonHandler):

	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def post(self):
		''' Sign-up with form inputs

		@param un:			String username (email address format)
		@param pw:			String password

		@param name:		String name ''' 

		p = self.get_params([
			('un', True, None),
			('pw', True, None),
			('name', True, None),			
		])

		# create new data
		data = {}
		data.update(p)
		user = HDUser(data=data)

		try:
			yield user.create_async()
		except pymongo.errors.DuplicateKeyError, e:
			raise HDError(domain='SignUpAPIHandler', errno=HDORMObject.ERR_NO_DATA,
					msg=r'Sign-in with ID and Password.')

		# create new session
		session = yield HDSession.login(iid=user.iid, ip=self.request.remote_ip)
		self.set_secure_cookie(name='sid', value=session.iid, expires_days=self.application.config['server']['session_expire_days'])
		
		self.finish_and_return(result=user.snapshot);

class SignInAPIHandler(CommonHandler):

	@tornado.web.asynchronous
	@authenticated_api
	@tornado.gen.coroutine
	def get(self):
		''' Log-in by session cookie '''

		self.finish_and_return(result=self.current_user.snapshot)

	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def post(self):
		''' Sign-in with username and password

		@param un:			String username (email address format)
		@param pw:			String password '''

		p = self.get_params([
			('un', True, None),
			('pw', True, None),
		])

		user = HDUser(data={'un': p['un'], 'pw': utils.get_hash_value(p['pw'])})
		yield user.read_async()
		if user.data is None:
			user = HDUser(data={'un': p['un']})
			yield user.read_async()
			if user.data is None:
				raise HDError(domain='SignInAPIHandler', errno=HDORMObject.ERR_NO_DATA,
						msg=r'Not exists user.')
			else:
				raise HDError(domain='SignInAPIHandler', errno=HDORMObject.ERR_NO_DATA,
						msg=r'Password is not correct.')

		# create new session
		session = yield HDSession.login(iid=user.iid, ip=self.request.remote_ip)
		self.set_secure_cookie(name='sid', value=session.iid, expires_days=self.application.config['server']['session_expire_days'])
		
		self.finish_and_return(result=user.snapshot);

class SignOutAPIHandler(CommonHandler):

	@tornado.web.asynchronous
	@authenticated_api
	@tornado.gen.coroutine
	def get(self):
		''' Sign out current session. '''
		yield tornado.gen.Task(self.current_session.logout)
		self.clear_cookie('sid')
		self.finish_and_return()

	@tornado.web.asynchronous
	@authenticated_api
	@tornado.gen.coroutine
	def post(self):
		''' Signout current session (same with GET) '''
		yield tornado.gen.Task(self.current_session.logout)
		self.clear_cookie('sid')
		self.finish_and_return()
		