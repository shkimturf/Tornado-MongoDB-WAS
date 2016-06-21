# -*- coding: utf-8 -*-
''' 
Created on 2016. 5. 23.

@author: Sunhong Kim
'''

import tornado.web, tornado.httpserver
from app import HDApp
import os, logging

from server.handlers.signing_handlers import SignUpAPIHandler, SignInAPIHandler, SignOutAPIHandler

class Server(tornado.web.Application):
	''' Tornado + mongoDB server template '''

	def __init__(self, hdapp=None):
		import models
		models.ensure_async_db_structure(hdapp=hdapp)
		
		self.hdapp = hdapp
		self.config = hdapp.config

		self.template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.config[self.hdapp.app_name]["template_dir"])
		self.static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.config[self.hdapp.app_name]["static_dir"])

		handlers  = [
			(r'/signup', SignUpAPIHandler),
		 	(r'/signin', SignInAPIHandler),
			(r'/signout', SignOutAPIHandler),
		]

		settings = dict(debug=self.config[self.hdapp.app_name]['debug'], template_path=self.template_dir, static_path=self.static_dir,
			cookie_secret=str(self.config[self.hdapp.app_name]['cookie_secret']), login_url='')
		tornado.web.Application.__init__(self, handlers, **settings)

    		logging.warning('Server is running now')

if __name__ == '__main__':
	hdapp = HDApp('server')

	port = hdapp.config[hdapp.app_name]['port']
	server = Server(hdapp=hdapp)
	http_server = tornado.httpserver.HTTPServer(server)
	http_server.listen(port)

	try:
		tornado.ioloop.IOLoop.instance().start()
	except (KeyboardInterrupt, SystemExit), e:
		tornado.ioloop.IOLoop.instance().stop()
		