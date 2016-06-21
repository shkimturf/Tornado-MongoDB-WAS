# -*- coding: utf-8 -*-
'''
Created on 2016. 5. 25.

@author: Sunhong Kim
'''

from app import HDApp
from models.orm import HDORMObject

import tornado, utils

class HDMongoAsyncObject(HDORMObject):
	''' Basic object using motor tools.

	It supports
		- Common data structures
		- Common properties and helper functions (CRUD) '''

	''' ORM(Object Related Method) CRUD functions '''
	@tornado.gen.coroutine
	def create_async(self):
		''' Write a row on DB asynchronously. '''

		hdapp = HDApp.shared_app
		col = hdapp.get_async_collection_conn(col_name=self._collection_name())

		self._check_data_validity()
		
		yield col.save(self.data)

		raise tornado.gen.Return(self)

	@tornado.gen.coroutine
	def read_async(self):
		''' Read object from DB asynchronously with my data. '''

		hdapp = HDApp.shared_app
		col = hdapp.get_async_collection_conn(col_name=self._collection_name())		
		
		spec = None
		if '_id' in self.data:
			spec = {'_id': self.iid}
		else:
			spec = self.data

		row = yield col.find_one(spec)
		if row is None:
			self.data = None
			raise tornado.gen.Return(None)

		self.data = row

		raise tornado.gen.Return(self)

	@tornado.gen.coroutine
	def update_async(self, document, do_refresh=False, do_update_timestamp=True):
		''' Update object from DB asynchronously. 

		@param document:			dictionary specifying the document to use for the update or insert. (ex: {'$set': {'un': 'Sunhong Kim'}})
		@param do_refresh:			update current object data or not.
		@param do_update_timestamp:	update timestamp or not.
		'''

		hdapp = HDApp.shared_app
		col = hdapp.get_async_collection_conn(col_name=self._collection_name())

		if do_update_timestamp:
			if '$set' in document.keys():
				document['$set']['_ts'] = utils.get_timestamp()
			else:
				document['$set'] = {'_ts': utils.get_timestamp()}
		yield col.update({'_id': self.iid}, document)
		
		if do_refresh:
			yield self.read_async()

		return 

	@tornado.gen.coroutine
	def delete_async(self):
		''' Delete object from DB asynchronously. '''

		hdapp = HDApp.shared_app
		col = hdapp.get_async_collection_conn(col_name=self._collection_name())

		yield col.remove({'_id': self.iid})

		return 
		