# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from Models.Config import Config
from Utils.utils import json_response, str_import
import URLs
from flask_cors import CORS, cross_origin

import flask_mail
from raven.contrib.flask import Sentry





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

mail = flask_mail.Mail()
mail.init_app(app=app)

sentry = Sentry(dsn='https://4e1a812ea958463fbda2cf92b8f111cc:53072bf456b144db88dbf8c7edbcf7ea@sentry.io/177217')
sentry.init_app(app)
routes = URLs.get_urls()

for route in routes:
    imported_class = str_import(routes[route]['class'])

    route_object = imported_class()
    app.add_url_rule(route, view_func=route_object.dispatcher, endpoint=routes[route]['endpoint'],
                     methods=['GET', 'POST', 'PUT', 'DELETE'])


#TODO app.register_error_handler()

from Utils import ExceptionHandler
from Utils.ExceptionHandler import error_dict, Handler

for e in error_dict:
    app.register_error_handler(e, Handler(e).generate_response)


# @app.errorhandler(404)
# @app.errorhandler(401)
@app.errorhandler(500)
@json_response
def page_not_found(error):
    return ExceptionHandler.BASIC_ERROR_500


if __name__ == "__main__":
    app.run('0.0.0.0')
