from mongoengine.errors import *
from Utils.utils import json_response
from flask import current_app as app
from Utils.Exceptions import Mongo, Bussiness
import inspect


error_dict = {}

class Handler:
    def __init__(self, e):
        self.e = e

    @json_response
    def generate_response(self, e):

        if hasattr(e,'code') and hasattr(e,'message'):
            self.error_code = e.code
            self.error_message = e.message
        else:
            self.error_code = error_dict[self.e]['error_code']
            self.error_message = error_dict[self.e]['error_message']

        if (self.e == Exception()):
            app.sentry.captureException()
        return {
            'error_code':self.error_code,
            'error_message':self.error_message
        }

def getErrorDict(selected_class):
    res = {}
    for name, obj in inspect.getmembers(selected_class):
        if inspect.isclass(obj):
            res[obj] = ''
    return res

error_dict.update(Mongo.errors)
error_dict.update(getErrorDict(Bussiness))
