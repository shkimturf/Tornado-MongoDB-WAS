# -*- coding: utf-8 -*-
'''
Created on 2016. 5. 25.

@author: Sunhong Kim
'''

from app import HDApp
from app.error import HDError

import utils, re, tornado, math
from utils import Property

from models.object import HDObject

class HDUser(HDObject):

	EMAIL_VALIDITY_PROG = re.compile("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$")

	''' class documents
	{
		'_id': 		String

		'un':		String
		'pw':		String

		'name':		String
	}
	'''

	@classmethod
	def _get_id_prefix(cls):
		return u'usr'

	@classmethod
	def _collection_name(cls):
		return u'user'

	def _check_data_validity(self):
		super (HDObject, self)._check_data_validity()
		
		if re.match(self.EMAIL_VALIDITY_PROG, self.data['un']) is None:
			raise HDError(domain='HDAccount', errno=HDObject.ERR_INVALID_DATA,
				msg=u'ID should be email format.')
		if len(self.data['pw']) < 4:
			raise HDError(domain='HDAccount', errno=HDObject.ERR_INVALID_DATA,
				msg=u'Password should be longer than 4.')
		if len(self.data['pw']) > 16:
			raise HDError(domain='HDAccount', errno=HDObject.ERR_INVALID_DATA,
				msg=u'Password should be shorter than 16.')
		
		self.data['pw'] = utils.get_hash_value(self.data['pw'])

	@Property
	def snapshot():
		doc = 'Snapshot of this user.'
		def fget(self):
			snapshot = {}
			snapshot.update(self.data)
			
			if 'un' in snapshot.keys():
				del snapshot['un']
			if 'pw' in snapshot.keys():
				del snapshot['pw']

			snapshot['_ts'] = utils.get_readable_date_from_timestamp(snapshot['_ts'])
			if '_cts' in snapshot.keys():
				snapshot['_cts'] = utils.get_readable_date_from_timestamp(snapshot['_cts'])

			return snapshot
		return locals()
		