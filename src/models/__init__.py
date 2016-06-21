# -*- coding: utf-8 -*-
'''
Created on 2016. 5. 25.

@author: Sunhong Kim
'''

import sys

def ensure_db_structure(hdapp):
	''' With a given hdapp, this function will try to ensure every things are in working condition,
	such as ensuring appropriate indexes. '''

	# Indexing collections
	from models.account.user import HDUser
	col = hdapp.get_collection_conn(col_name=HDUser._collection_name())
	col.ensure_index('un', unique=True, background=True, sparse=True)

	from models.account.session import HDSession
	col = hdapp.get_collection_conn(col_name=HDSession._collection_name())
	col.ensure_index('aid', background=True)

def ensure_async_db_structure(hdapp):
	''' With a given hdapp, this function will try to ensure every things are in working condition,
	such as ensuring appropriate indexes. '''

	# Indexing collections
	from models.account.user import HDUser
	col = hdapp.get_async_collection_conn(col_name=HDUser._collection_name())
	col.ensure_index('un', unique=True, background=True, sparse=True)

	from models.account.session import HDSession
	col = hdapp.get_async_collection_conn(col_name=HDSession._collection_name())
	col.ensure_index('aid', background=True)
	