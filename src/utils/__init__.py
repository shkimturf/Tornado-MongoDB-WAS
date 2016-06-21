# -*- coding: utf-8 -*-
import time
import datetime
import dateutil.parser

def get_hash_value(value):
	''' Generate hashed value from a given value. 
	Use SHA256 + Base64 encoding to encrypt password.
	'''
	from Crypto.Hash import SHA256
	import base64

	h = SHA256.new()
	h.update(value)
	enc = h.digest()
	return base64.b64encode(enc)

def generate_internal_id(prefix=''):
	''' Generate internal ID with a given prefix. '''
	import bson
	newid = bson.ObjectId()
	return '%s%s' % (prefix, str(newid))

def get_timestamp():
	''' Returns unix-style timestamp (milliseconds) in UTC. '''
	t = datetime.datetime.utcnow()
	return int(time.mktime(t.timetuple())*1e3 + t.microsecond/1e3)

def get_readable_current_timestamp():
	''' Returns readable time string for current time '''
	readable_time = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
	return readable_time

def Property(func):
	''' Decorator for properties. See details at 
	http://code.activestate.com/recipes/410698/ '''	
	return property(**func())

def get_readable_date_from_timestamp(timestamp):
	date = datetime.datetime.fromtimestamp(timestamp / 1000)
	return '%04d-%02d-%02dT%02d:%02d:%02d' % (date.year, date.month, date.day,
								date.hour, date.minute, date.second)

def get_timestamp_from_readable_date(date):
	t = dateutil.parser.parse(date)
	return int(time.mktime(t.timetuple())*1e3 + t.microsecond/1e3)
