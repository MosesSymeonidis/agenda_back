from flask import jsonify
from mongoengine import Document
from bson import objectid
from datetime import datetime
from pymongo.cursor import Cursor
import json
from flask import current_app as app
from mongoengine import connect
from threading import Thread


def bson_handler(x):
    """
    Handles bson types for json dumps for the framework
    :param x: The attribute of the object
    :return: The 'translated' attribute with proper format
    """
    if isinstance(x, datetime):
        return x.isoformat()
    elif x in [True,False]:
        if x :
            return 'True'
        else:
            return 'False'

    elif isinstance(x, objectid.ObjectId):
        return str(x)
    elif callable(getattr(x, "to_mongo", None)):
        return x.to_mongo()
    elif isinstance(x, str):
        return x
    elif isinstance(x, Exception):
        print(x.errno, x.strerror)
        return {
            'error': x.strerror,
            'error_number': x.errno
        }
    else:
        return str(x)
        raise TypeError(x)


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
    client = connect(host=app.config['MONGODB_STRING'], db=app.config['MONGODB_DATABASE'])
    return client[app.config['MONGODB_DATABASE']]


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