# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from Models.Config import Config
from Utils.utils import json_response, str_import
import URLs
from flask_cors import CORS, cross_origin

from flask_mail import Mail


db = MongoEngine()
app = Flask(__name__)
CORS(app)
app.config['MONGODB_SETTINGS'] = {
    'db': 'my_app_database',
    'host': 'mongodb://cbuser:092hdfkv245@ds053305.mlab.com:53305/cheapbookdev'
}

db.init_app(app)

app.session_interface = MongoEngineSessionInterface(db)
configs = Config.objects.get(config_id='initials')
app.config.from_object(configs)
app.config['DEBUG']=False
routes = URLs.get_urls(debug=app.config.get('DEBUG'))

for route in routes:
    imported_class = str_import(routes[route]['class'])

    route_object = imported_class()
    app.add_url_rule(route, view_func=route_object.dispatcher, endpoint=routes[route]['endpoint'],
                     methods=['GET', 'POST', 'PUT', 'DELETE'])


#TODO app.register_error_handler()

from Utils.ExceptionHandler import error_dict, Handler

for e in error_dict:
    app.register_error_handler(e, Handler(e).generate_response)


# @app.errorhandler(404)
# @app.errorhandler(401)
# @app.errorhandler(500)
# @json_response
# def page_not_found(error):
#     error_handler = ErrorHandler(error=error)
#     return error_handler.response()
#     if hasattr(error, 'code'):
#         return {'error': error.code, 'description': error.description}
#     from mongoengine import errors as mongoerrors
#     base_class = error.__class__.__bases__[0]
#     if base_class.__name__ in mongoerrors.__all__:
#         if base_class == mongoerrors.DoesNotExist:
#
#             print(error.__class__)
#             print(error)
#             print(error.code)
#             return {'error':'document does not exists'}
#         print('mongoerror')
#     return {'error': str(error)}


if __name__ == "__main__":
    app.run('0.0.0.0')
