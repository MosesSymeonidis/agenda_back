from mongoengine.errors import *
from utils.base import json_response
from flask import current_app as app
from utils.exceptions import mongo, business
import inspect

error_dict = {}


class Handler:
    def __init__(self, e):
        self.e = e

    @json_response
    def generate_response(self, e):
        self.error_parameters = {}
        if hasattr(e, 'code') and hasattr(e, 'message'):
            self.error_code = e.code
            self.error_message = e.message
            if hasattr(e, 'parameters'):
                self.error_parameters = e.parameters

        else:
            self.error_code = error_dict[self.e]['error_code']
            self.error_message = error_dict[self.e]['error_message']

        if (self.e == Exception()):
            app.sentry.captureException()
        return {
            'error_code': self.error_code,
            'error_message': self.error_message,
            'error_parameters': self.error_parameters
        }


def getErrorDict(selected_class):
    res = {}
    for name, obj in inspect.getmembers(selected_class):
        if inspect.isclass(obj):
            res[obj] = ''
    return res


error_dict.update(mongo.errors)
error_dict.update(getErrorDict(business))
