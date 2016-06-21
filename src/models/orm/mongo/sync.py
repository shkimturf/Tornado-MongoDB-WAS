# -*- coding: utf-8 -*-
'''
Created on 2016. 5. 25.

@author: Sunhong Kim
'''

from app import HDApp
from models.orm import HDORMObject

import utils

class HDMongoSyncObject(HDORMObject):
	''' Basic object using pymongo tools.

	It supports
		- Common data structures
		- Common properties and helper functions (CRUD) '''

	''' ORM(Object Related Method) CRUD functions '''
	def create(self):
		''' Write a row on DB synchronously. '''

		hdapp = HDApp.shared_app
		col = hdapp.get_collection_conn(col_name=self._collection_name())

		self._check_data_validity()

		col.save(self.data)

		return self

	def read(self):
		''' Read object from DB synchronously with my data. '''

		hdapp = HDApp.shared_app
		col = hdapp.get_collection_conn(col_name=self._collection_name())

		spec = None
		if '_id' in self.data:
			spec = {'_id': self.iid}
		else:
			spec = self.data

		row = col.find_one(spec)
		if row is None:
			self.data = None
			return None

		self.data = row
		return self

	def update(self, document, do_refresh=False, do_update_timestamp=True):
		''' Update object from DB synchronously. 

		@param document:			dictionary specifying the document to use for the update or insert. (ex: {'$set': {'un': 'Sunhong Kim'}})
		@param do_refresh:			update current object data or not.
		@param do_update_timestamp:	update timestamp or not.
		'''

		hdapp = HDApp.shared_app
		col = hdapp.get_collection_conn(col_name=self._collection_name())

		if do_update_timestamp:
			if '$set' in document.keys():
				document['$set']['_ts'] = utils.get_timestamp()
			else:
				document['$set'] = {'_ts': utils.get_timestamp()}
		col.update({'_id': self.iid}, document)
		
		if do_refresh:
			self.read()

	def delete(self):
		''' Delete object from DB synchronously. '''

		hdapp = HDApp.shared_app
		col = hdapp.get_collection_conn(col_name=self._collection_name())

		col.remove({'_id': self.iid})
