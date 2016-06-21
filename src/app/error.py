# -*- coding: utf-8 -*-
'''
Created on 2016. 5. 23.

@author: Sunhong Kim
'''

class HDError(Exception):
	''' HDError class holds detailed and structured error information of internal system. '''

	def __init__(self, domain, errno, msg=None, trace=None):
		''' Construct HDError object

		@param domain: 	String specified where this exception occured.
		@param errno:	Integer error number. Constant defined in HDError
		@param msg:		String specified message. If msg is not given, default message will be used.
		@param trace:	List of traceback strings that can further specify detailed scenario. '''

		if msg is None:
			self.msg = u'No error message specified.'
		else:
			self.msg = msg

		self.errno = errno
		self.trace = []
		if trace is not None:
			self.add_trace(trace)

	def is_for_client(self):
		''' Return YES if this error is for client. otherwise NO.
		If this returns NO, it will cause server error. '''
		return self.errno < 0

	def add_trace(self, trace):
		''' Add trace string. Using this, you can see a list of personalized trace string.
		Also you can send Exception object to trace. '''
		self.trace.append(trace)

	def __str__(self):
		trace_msg = ''
		for trace in self.trace:
			try:
				if isinstance(trace, Exception):
					trace_msg = trace_msg + ('\n\t' + repr(trace))
				else:
					trace_msg = trace_msg + ('\n\t' + str(trace))
			except:
				trace_msg = trace_msg + '\n\tunprintable trace item.'

		if len(self.trace) > 0:
			return '[%d] %s\nTraces: \n%s' % (self.errno, self.msg, trace_msg)
		else:
			return '[%d] %s' % (self.errno, self.msg)
	