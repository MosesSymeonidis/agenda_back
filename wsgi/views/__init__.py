from Utils.utils import json_response
from flask.views import MethodView
from flask import request
class BaseView( MethodView ):
    def __init__(self):

        self.request = request


    @json_response
    def dispatcher(self,**kwargs):
        if self.request.method == 'GET':
            return self.get(**kwargs)

        elif self.request.method == 'POST':
            return self.post(**kwargs)

        elif self.request.method == 'PATCH':
            return self.patch(**kwargs)

        elif self.request.method == 'PUT':
            return self.put(**kwargs)

        elif self.request.method == 'DELETE':
            return self.delete(**kwargs)

    def get(self,**kwargs):
        return "ECHO: GET\n"

    def post(self,**kwargs):
        return "ECHO: POST\n"

    def patch(self,**kwargs):
        return "ECHO: PACTH\n"

    def put(self, **kwargs):
        return "ECHO: PUT\n"

    def delete(self,**kwargs):
        return "ECHO: DELETE"
