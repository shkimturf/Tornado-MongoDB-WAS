# -*- coding: utf-8 -*-
'''
Created on 2016. 5. 25.

@author: Sunhong Kim
'''

from models.object import HDObject
from app.error import HDError
from app import HDApp

import utils
from utils import Property

from models.account.user import HDUser
import tornado

class HDSession(HDObject):

	ERR_SESSION_EXPIRED					= -400
	ERR_NO_SUCH_SESSION					= -401

	@classmethod
	def _get_id_prefix(cls):
		return u's'

	@classmethod
	def _collection_name(cls):
		return u'session'

	@tornado.gen.coroutine
	def ensure_not_expired(self):
		''' Ensure that this session is not expired.
		If expired, session info on database will set to be expired also.
		Exception will be raised when expired. '''

		expired = False
		if self.data['expired']:
			expired = True
		elif utils.get_timestamp() >= self.data['expires']:
			expired = True
			yield self.update_async({'$set': {'expired': True}})
			self.data['expired'] = True

		if expired:
			raise HDError(domain='HDSession', errno=HDSession.ERR_SESSION_EXPIRED,
				msg=u'Session was expired.')
		
		return

	@tornado.gen.coroutine
	def log_accessed_from_ip(self, ip):
		''' Add in session access log on database '''

		if ip not in self.data['ip']:
			self.data['ip'].append(ip)
			yield self.update_async({'$push': {'ip': ip}})
		
		return

	@classmethod
	@tornado.gen.coroutine
	def login(cls, iid, ip):
		''' Create a new session with user ID

		@param iid:		String UserID
		@param ip:		String IP address which connection was made. '''

		session = HDSession(data={'uid': iid, 'expired': False})
		hdapp = HDApp.shared_app
		expires_time = utils.get_timestamp() + 60 * 60 * 24 * hdapp.config[hdapp.app_name]['session_expire_days'] * 1000
		
		yield session.read_async()
		if session.data is not None:
			yield session.update_async({'$set': {'expires': expires_time}})
		else:
			session = HDSession(data={
				'uid': iid,
				'ip': [str(ip)],
				'expired': False,
				'expires': expires_time,
			})
			yield session.create_async()
		
		raise tornado.gen.Return(session)

	@tornado.gen.coroutine
	def logout(self):
		''' Logout current session '''

		yield self.update_async({'$set': {'expired': True}})
		self.data['expired'] = True

		return

	@Property
	def user_id():
		doc = 'User ID of this session owner'
		def fget(self):
			return self.data['uid']
		return locals()
		