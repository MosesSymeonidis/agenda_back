from flask import jsonify
from mongoengine.queryset.queryset import QuerySet
from bson import objectid
from datetime import datetime
from werkzeug.routing import BaseConverter, UUIDConverter, ValidationError
import os
import tempfile
import json
from flask import current_app as app
from mongoengine import connect, DoesNotExist, Document
from threading import Thread

import inspect

def bson_handler(x):
    """
    Handles bson types for json dumps for the framework
    :param x: The attribute of the object
    :return: The 'translated' attribute with proper format
    """
    if isinstance(x, datetime):
        return x.isoformat()
    elif x in [True, False]:
        if x:
            return 'True'
        else:
            return 'False'
    elif isinstance(x, objectid.ObjectId):
        return str(x)
    elif callable(getattr(x, "to_mongo", None)):
        return x.to_mongo()
    elif isinstance(x, QuerySet):
        res = []
        for i in x:
            res.append(i.to_mongo(fields=x._loaded_fields.fields))
        return res
    elif isinstance(x, str):
        return x
    elif isinstance(x, list):
        res = []
        for i in x:
            res.append(bson_handler(i))
        return res
    elif isinstance(x, Exception):
        return {
            'error': x.strerror,
            'error_number': x.errno
        }
    else:
        return str(x)


def json_response(func):
    """
    Returns the json response of one view
    :param func: The view function
    :return: The json response
    """

    def func_wrapper(*args, **kwargs):
        return jsonify(json.loads(json.dumps(obj=func(*args, **kwargs), default=bson_handler)))

    return func_wrapper


def str_import(name):
    """
    Gets the name of the view and returns the appropriate function
    :param name: the path of the view eg 'views.test.test'
    :return: The class of the view
    """
    components = name.split('.')
    mod = __import__(".".join(components[:-1]), fromlist=[components[-1]])
    str_class = getattr(mod, components[-1])
    return str_class


def get_database():
    """
    Returns the client object of mongodb
    :return: client object of mongodb
    """
    client = connect(host=app.config['MONGODB_SETTINGS']['host'], db=app.config['MONGODB_SETTINGS']['db'])
    return client[app.config['MONGODB_SETTINGS']['db']]


def async(f):
    """
    decorator for async execution
    :param f:
    :return:
    """

    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


def save_request(request):
    req_data = {}
    req_data['endpoint'] = request.endpoint
    req_data['method'] = request.method
    req_data['cookies'] = request.cookies
    req_data['data'] = request.data
    req_data['headers'] = dict(request.headers)
    req_data['headers'].pop('Cookie', None)
    req_data['args'] = request.args
    req_data['form'] = request.form
    req_data['remote_addr'] = request.remote_addr
    req_data['url'] = request.url
    files = []
    for name, fs in request.files.items():
        dst = tempfile.NamedTemporaryFile()
        fs.save(dst)
        dst.flush()
        filesize = os.stat(dst.name).st_size
        dst.close()
        files.append({'name': name, 'filename': fs.filename, 'filesize': filesize,
                      'mimetype': fs.mimetype, 'mimetype_params': fs.mimetype_params})
    req_data['files'] = files

    return json.loads(json.dumps(obj=req_data, default=bson_handler))


def save_response(resp):
    resp_data = {}
    resp_data['status_code'] = resp.status_code
    resp_data['status'] = resp.status
    resp_data['headers'] = dict(resp.headers)
    resp_data['data'] = resp.response
    return json.loads(json.dumps(obj=resp_data, default=bson_handler))



class ModelConverter(BaseConverter):
    def __init__(self,map, model=None):
        import models
        BaseConverter.__init__(self, map)
        self.model = None
        if model in dir(models):

            temp_class = getattr(models, model)

            if inspect.isclass(temp_class) and issubclass(temp_class, Document):
                self.model = temp_class

    def to_python(self, value):

        if self.model:
            try:
                return self.model.objects.get(id=value)
            except:
                raise ValidationError()
        raise ValidationError()

    def to_url(self, value):
        if isinstance(value, self.model):
            value = value.id
        return super(ModelConverter, self).to_url(value)

