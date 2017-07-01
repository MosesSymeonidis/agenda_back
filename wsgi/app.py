# -*- coding: utf-8 -*-
import flask_mail
from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from raven.contrib.flask import Sentry
from Utils.Exceptions import GeneralExceptions
import URLs
from Models.Utils import Config, Traffic
from Utils.utils import json_response, str_import, save_request, save_response
from flask import request
from flask import g as global_storage
import flask_mobility

db = MongoEngine()
app = Flask(__name__)
CORS(app)
app.config['MONGODB_SETTINGS'] = {
    'db': 'cheapbookdev',
    'host': 'mongodb://cbuser:092hdfkv245@ds053305.mlab.com:53305/cheapbookdev'
}

db.init_app(app)

configs = Config.objects.get(config_id='initials')
app.config.from_object(configs)
app.config['DEBUG']=False

mail = flask_mail.Mail()
mail.init_app(app=app)

sentry = Sentry(dsn='https://4e1a812ea958463fbda2cf92b8f111cc:53072bf456b144db88dbf8c7edbcf7ea@sentry.io/177217')
sentry.init_app(app)
flask_mobility.Mobility().init_app(app=app)

routes = URLs.get_urls()

for route in routes:
    imported_class = str_import(routes[route]['class'])

    route_object = imported_class()
    app.add_url_rule(route, view_func=route_object.dispatcher, endpoint=routes[route]['endpoint'],
                     methods=['GET', 'POST', 'PUT', 'DELETE'])


from Utils.ExceptionHandler import error_dict, Handler

for e in error_dict:
    app.register_error_handler(e, Handler(e).generate_response)


# @app.errorhandler(404)
# @app.errorhandler(401)
@app.errorhandler(500)
@json_response
def page_not_found(error):
    return GeneralExceptions.BASIC_ERROR_500

@app.errorhandler(404)
@json_response
def page_not_found(error):
    return GeneralExceptions.BASIC_ERROR_500

@app.before_request
def before_request():
    request_data = save_request(request)
    global_storage.request_data=request_data


@app.after_request
def after_request(resp):
    resp_data = save_response(resp)
    request_data = global_storage.request_data
    traffic = Traffic(request=request_data,response=resp_data)
    traffic.save()
    return resp

if __name__ == "__main__":
    app.run('0.0.0.0')
