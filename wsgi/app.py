# -*- coding: utf-8 -*-
import flask_mail
from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from raven.contrib.flask import Sentry
import URLs
from utils.base import json_response, str_import, save_request, save_response
from flask import request
from flask import g as global_storage
import flask_mobility
from utils.base import generate_model_converter
from mongoengine import Document


def create_app( is_sentry_on=False, **kwargs):
    app = Flask(__name__)

    app.config.update(kwargs or {})


    db=MongoEngine()

    CORS(app)

    if 'TESTING' in kwargs and kwargs['TESTING']:
        app.testing = True

        db.init_app(app, {'MONGODB_SETTINGS':
                              {
                                'db': 'testing',
                                'host': 'mongodb://testuser:21132113@ds111876.mlab.com:11876/testing'
                              }
        }
                    )
        # db.connection
    else:
        app.config['MONGODB_SETTINGS'] = {
            'db': 'cheapbookdev',
            'host': 'mongodb://cbuser:092hdfkv245@ds053305.mlab.com:53305/cheapbookdev'
        }
        db.init_app(app)

    import models
    configs = models.Config.objects.get(config_id='initials')
    app.config.from_object(configs)
    app.config['DEBUG']=False


    mail = flask_mail.Mail()
    mail.init_app(app=app)
    if is_sentry_on:
        sentry = Sentry(dsn='https://4e1a812ea958463fbda2cf92b8f111cc:53072bf456b144db88dbf8c7edbcf7ea@sentry.io/177217')
        sentry.init_app(app)
    flask_mobility.Mobility().init_app(app=app)

    from utils.exception_handler import error_dict, Handler

    for e in error_dict:
        app.register_error_handler(e, Handler(e).generate_response)
    from utils.exceptions import general_exceptions

    # @app.errorhandler(404)
    # @app.errorhandler(401)
    @app.errorhandler(500)
    @json_response
    def page_not_found_500(error):
        return general_exceptions.BASIC_ERROR_500

    @app.errorhandler(404)
    @json_response
    def page_not_found_404(error):
        return general_exceptions.BASIC_ERROR_500

    @app.before_request
    def before_request():
        request_data = save_request(request)
        global_storage.request_data=request_data


    @app.after_request
    def after_request(resp):
        resp_data = save_response(resp)
        request_data = global_storage.request_data
        traffic = models.Traffic(request=request_data,response=resp_data)
        traffic.save()
        return resp

    routes = URLs.get_urls()
    print(dir(models))
    import inspect
    for i in dir(models):
        temp_class = getattr(models,i)
        if inspect.isclass(temp_class) and issubclass(temp_class, Document):

            app.url_map.converters[i.lower()] = generate_model_converter(temp_class)


    for route in routes:
        imported_class = str_import(routes[route]['class'])

        route_object = imported_class()
        app.add_url_rule(route, view_func=route_object.dispatcher, endpoint=routes[route]['endpoint'],
                         methods=['GET', 'POST', 'PUT', 'DELETE'])

    return app

if __name__ == "__main__":
    create_app(MONGODB_SETTINGS = {
        'db': 'cheapbookdev',
        'host': 'mongodb://cbuser:092hdfkv245@ds053305.mlab.com:53305/cheapbookdev'
    }).run('0.0.0.0')
