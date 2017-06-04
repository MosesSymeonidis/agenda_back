# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from Models.Config import Config
from Utils.utils import json_response, str_import
import URLs

from flask_mail import Mail


db = MongoEngine()
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'my_app_database',
    'host': 'mongodb://cbuser:092hdfkv245@ds053305.mlab.com:53305/cheapbookdev'
}

db.init_app(app)

app.session_interface = MongoEngineSessionInterface(db)
configs = Config.objects.get(config_id='initials')
app.config.from_object(configs)

print(configs.to_json())
print(app.config.get('DEBUG'))
routes = URLs.get_urls(debug=app.config.get('DEBUG'))

for route in routes:
    imported_class = str_import(routes[route])
    route_object = imported_class()
    app.add_url_rule(route, view_func=route_object.dispatcher, endpoint=routes[route],
                     methods=['GET', 'POST', 'PUT', 'DELETE'])


@app.errorhandler(404)
@app.errorhandler(401)
@app.errorhandler(500)
@json_response
def page_not_found(error):
    try:
        return {'error': error.code, 'description': error.description}
    except Exception as e:
        return {'error': str(e)}


if __name__ == "__main__":
    app.run('0.0.0.0')
