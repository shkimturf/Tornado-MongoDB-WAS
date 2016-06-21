# -*- coding: utf-8 -*-
'''
Created on 2016. 5. 25.

@author: Sunhong Kim
'''

from models.orm.mongo.sync import HDMongoSyncObject
from models.orm.mongo.async import HDMongoAsyncObject

class HDObject(HDMongoSyncObject, HDMongoAsyncObject):
	''' Basic object using on service. 
	Supports sync / async database operations by multiple inheritance. '''

	ERR_INVALID_DATA			= -120
	pass