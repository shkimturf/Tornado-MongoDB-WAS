# -*- coding: utf-8 -*-
'''
Created on 2016. 5. 16.

@author: Sunhong Kim
'''

import pymongo

import motor.motor_tornado as motor

from utils.config import Config
from utils import Property

class HDApp(object):
	''' HDApp is a utility framework which every independent Project Kuo application should use.
	It provided as a singleton base.

	Main functionalities
	- Reading configuration upon initialize and provide them easily.
	- Connect, provide and cache database connections.
	'''

	shared_app = None

	def __init__(self, app_name=None, config_file_path=None):
		''' Initialize with config options '''

		if app_name is not None:
			self.app_name = app_name

		self.config = Config(config_file_path=config_file_path)

		# dbcon will share connections to the database and collections
		self.dbcon = {}

		# Connection to mongoDB
		self._mongo_db = None
		# Asynchronous connection to mongoDB
		self._async_mongo_db = None

		# To use this as a singleton, set it to method variable.
		# WARNING: It does not strictly implement singleton, but use it at own risk.
		HDApp.shared_app = self

	''' Synchronous DB connections '''
	def get_collection_conn(self, col_name, db_name=None):
		''' Returns mongoDB collection connection.
		If db_name is passes as None, it'll read default database specified in the configuration. '''

		if db_name is None:
			db_name = self.config[self.app_name]['database']['db_name']

		if db_name not in self.dbcon:
			db_con = pymongo.database.Database(self.mongo_db, db_name)
			# Store database connection
			self.dbcon[db_name] = {'___dbcon___':db_con}

		if col_name not in self.dbcon[db_name]:
			col_con = pymongo.collection.Collection(self.dbcon[db_name]['___dbcon___'], col_name)
			# Store collection connection
			self.dbcon[db_name][col_name] = col_con

		return self.get_db_conn(db_name=db_name)[col_name]

	def get_db_conn(self, db_name=None):
		''' Returns mongoDB database connection.
		If db_name is passes as None, it'll read default database specified in the configuration. '''

		if db_name is None:
			db_name = self.config[self.app_name]['database']['db_name']

		if db_name not in self.dbcon:
			db_con = pymongo.database.Database(self.mongo_db, db_name)
			# Store database connection
			self.dbcon[db_name] = {'___dbcon___':db_con}

		return self.dbcon[db_name]['___dbcon___']

	@Property
	def mongo_db():
		doc = "Application-wide mongo DB connection"
		def fget(self):
			if self._mongo_db is None:
				self._mongo_db = pymongo.Connection(self.config[self.app_name]['database']['host'], 
					int(self.config[self.app_name]['database']['port']))
			return self._mongo_db
		return locals()

	def disconnect_database(self):
		''' Disconnect current mongoDB connection '''

		if self._mongo_db is not None:
			self.mongo_db.close()
			self._mongo_db = None
			self.dbcon = {}

	''' Asynchronous connections '''
	def get_async_collection_conn(self, col_name, db_name=None):
		''' Returns asynchronous mongoDB connection.
		If db_name is passes as None, it'll read default database specified in the configuration. '''
		
		if db_name is None:
			db_name = self.config[self.app_name]['database']['db_name']

		return self.async_mongo_db[db_name][col_name]

	def get_async_db_conn(self, db_name=None):
		''' Returns asynchronous mongoDB connection.
		If db_name is passes as None, it'll read default database specified in the configuration '''

		if db_name is None:
			db_name = self.config[self.app_name]['database']['db_name']

		self.async_mongo_db[db_name]

	@Property
	def async_mongo_db():
		doc = 'Applicatoin-wide asynchronous mongo DB connection '
		def fget(self):
			if self._async_mongo_db is None:
				self._async_mongo_db = motor.MotorClient(self.config[self.app_name]['database']['host'],
					int(self.config[self.app_name]['database']['port']))
			return self._async_mongo_db
		return locals()
		