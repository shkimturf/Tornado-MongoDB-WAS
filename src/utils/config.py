# -*- coding: utf-8 -*-
'''
Created on 2016. 5. 16.

@author: Sunhong Kim
''' 

import os, yaml

class Config(object):
	''' Reading configuration file to use as option.
	Load consts file using pyyaml (to install: pip install pyyaml)
	'''

	def __init__(self, config_file_path=None):
		''' Load config file using pyyaml (to install: pip install pyyaml) '''
		if not config_file_path:
			config_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config/default.yaml')

		config_file = open(config_file_path)
		self.consts = yaml.safe_load(config_file)
		config_file.close()

	def __getitem__(self, prop):
		''' Provides dictionary style getter '''
		return self.consts[prop]