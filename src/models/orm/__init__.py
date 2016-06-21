# -*- coding: utf-8 -*-
'''
Created on 2016. 5. 25.

@author: Sunhong Kim
'''

import utils
from utils import Property

from app.error import HDError

class HDORMObject(object):
	''' Basic object using on service.

	It supports
		- Common data structures
		- Common properties and helper functions (CRUD) '''

	ERR_NO_DATA				= -100
	ERR_ID_MISSED				= -101
	ERR_INVALID_VALUE			= -102

	def __init__(self, data=None, iid=None):
		self.data = data
		if data is None and iid is not None:
			self.data = {'_id': iid}

	@classmethod
	def _get_id_prefix(cls):
		''' ID prefix for using on DB '''
		raise NotImplementedError

	@classmethod
	def _collection_name(cls):
		''' Collection name to read/write on DB. '''
		raise NotImplementedError

	''' Helper functions '''
	def _generate_internal_id(self):
		return utils.generate_internal_id(prefix=self._get_id_prefix())

	def _check_data_validity(self):
		if self.data is None:
			raise HDError(domain='HDORMObject', errno=HDORMObject.ERR_NO_DATA,
				msg=u'Set data first to check data.')

		if '_id' not in self.data:
			self.data['_id'] = self._generate_internal_id()
		if not self.data.has_key('_ts'):
			self.data['_ts'] = utils.get_timestamp()
		if not self.data.has_key('_cts'):
			self.data['_cts'] = utils.get_timestamp()
			
	@Property
	def iid():
		doc = 'ID of this object.'
		def fget(self):
			try:
				return self.data['_id']
			except Exception, e:
				raise HDError(domain='HDORMObject', errno=HDORMObject.ERR_ID_MISSED,
						msg=u'Object ID missed')
		return locals()

	@Property
	def snapshot():
		doc = 'Snapshot of this object. Data structure which client can see.'
		def fget(self):
			snapshot = {}
			snapshot.update(self.data)
			snapshot['_ts'] = utils.get_readable_date_from_timestamp(snapshot['_ts'])
			if '_cts' in snapshot.keys():
				snapshot['_cts'] = utils.get_readable_date_from_timestamp(snapshot['_cts'])

			return snapshot
		return locals()
	