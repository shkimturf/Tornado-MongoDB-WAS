# Tornado+MongoDB-WAS

Template server based python tornado using mongo database.

This template has been implemented below features.

 1. Asynchronous connections on mongoDB and use it on operation.
 2. Perform asynchronous authentications using decorator (@authenticated_api)
 3. ORM designed models that supports CRUD functions. (mongoDB only. If you want to use other database platform, inherit HDORMObject with driver)
 4. Config server environment with configuration file (default.yaml)
 5. Supports some kinds of utilities (utils)

## Environments

Python 2.7

## Dependent modules

There are some modules to run this templates.
Run below shell script to install python modules

```
    pip install tornado
    pip install pymongo
    pip install motor
    pip install pyyaml
    pip install pycrypto
    pip install apscheduler
    pip install python-dateutil
```

## Run templates

Set $PYTHONPATH to src folder absolute path and run src/server/main.py

## Usage

### Config

Set your customized config values on config/default.yaml

```
    port: 8080

        session_expire_days: 1

        template_dir: templates/
        static_dir: statics/
        favicon_path: favicon/

        cookie_secret: cookie_secret_here

        database:
            host: 127.0.0.1
            port: 5000

            db_name: db_name

        debug: 1
```

### Authentications

You can support authenticated handler easily by placing some decorators to support authenticated API or some script.

``` python
    @tornado.web.asynchronous
    @authenticated_api
    @tornado.gen.coroutine
    class AuthenticatedAPIHandler(CommonHandler):

    	print self.current_user # returns HDUser instance
    	self.finish_and_return()

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    class UnDecoratedAuthenticatedAPIHandler(CommonHandler):
	
    	yield self.get_current_user()
    	if self.current_user is not None:
    		# authenticated
    		# do something
    		pass
    	else:
    		raise tornado.web.HTTPError(403)
```

### CRUD

Inherit HDMongoSyncObject or HDMongoAsyncObject to support CRUD.

Use HDMongoAsyncObject on tornado server IOLoop to support asynchronous database connections.

If you want to use other database platform, inherit HDORMObject and implement CRUD functions.

## Author

[shkimturf](https://github.com/shkimturf)

## License

Tornado+MongoDB-WAS is under MIT License.