from views import BaseView
from Utils.Validation import RequestValidation

from Models.User import User

auth = User.auth

from flask import g as global_storage


class User(BaseView):

    @RequestValidation.parameters_assertion(parameters=['id'])
    def get(self):
        id = self.request.args['id']
        user = User.objects.get(pk=id)
        return user.to_mongo(fields=['_id', 'username'])

    @RequestValidation.parameters_assertion(parameters=['name', 'password'])
    def post(self):
        name = self.request.args['name']
        password = self.request.args['password']
        user = User()
        user.set_username_and_password(name, password)
        user.save()
        return user.to_mongo(fields=['_id'])

    @auth.login_required
    @RequestValidation.parameters_assertion(parameters=['password'])
    def put(self):
        password = self.request.args['password']
        user = global_storage.user

        user.assertion_is_activated()
        user.assertion_is_not_deleted()

        user.set_password(password)
        user.save()

        return user.to_mongo(fields=['_id'])

    @auth.login_required
    def delete(self):
        user = global_storage.user
        user.assertion_is_not_deleted()

        user.marked_as_deleted()
        return {'ok': True}


class Login(BaseView):
    @auth.login_required
    def get(self):
        user = global_storage.user

        user.assertion_is_not_deleted()
        user.assertion_is_activated()

        token = user.generate_auth_token(600)
        return {'token': token.decode('ascii'), 'duration': 600}


class Activation(BaseView):

    @RequestValidation.parameters_assertion(parameters=['activation_code'])
    def get(self, **kwargs):
        user = User.objects.get(pk=kwargs['user_id'])
        res = user.verify_activation(self.request.args.get('activation_code'))

        return { 'ok': res}

    @auth.login_required
    def post(self):
        user = global_storage.user
        user.assertion_is_not_deleted()
        #TODO resend activation mail
        return {'success':True}

class Role(BaseView):

    @auth.login_required
    def post(self, **kwargs):
        role = kwargs['role']
        user = global_storage.user
        user.assertion_is_not_deleted()



