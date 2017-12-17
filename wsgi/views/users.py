from views import BaseView
from utils.validation import RequestValidation
import models

auth = models.User.auth
from flask import render_template
from flask import g as global_storage


class UserView(BaseView):

    @RequestValidation.parameters_assertion(parameters=['username', 'password', 'email'],args_or_form='json')
    def post(self, **kwargs):
        name = self.request.get_json()['username']
        password = self.request.get_json()['password']
        email = self.request.get_json()['email']
        user = models.User()
        user.set_credentials(username=name,email=email, password=password)
        role = kwargs['role'] if 'role' in kwargs else models.User.GUEST_ROLE
        if role:
            user.role = role
        user.save()
        activation_code = user.generate_activation_code()

        res = render_template('mails/activation_mail.html', user_id = user.id,activation_code = activation_code)
        print(res)

        return user.to_mongo(fields=['_id'])


    @RequestValidation.parameters_assertion(parameters=['id'])
    def get(self):
        id = self.request.args['id']
        user = models.User.objects.get(pk=id)
        return user.to_mongo(fields=['_id', 'username'])


    @auth.login_required
    @RequestValidation.parameters_assertion(parameters=['password'])
    def put(self, **kwargs):
        password = self.request.args['password']
        user = global_storage.user

        user.assertion_is_activated()
        user.assertion_is_not_deleted()
        role = kwargs['role'] if 'role' in kwargs else models.User.GUEST_ROLE
        if role:
            user.roles = [role]

        user.set_password(password)
        user.save()

        return user.to_mongo(fields=['_id'])

    @auth.login_required
    def delete(self):
        user = global_storage.user
        user.assertion_is_not_deleted()

        user.marked_as_deleted()
        return {'ok': True}


class token(BaseView):
    @auth.login_required
    def post(self):
        user = global_storage.user

        user.assertion_is_not_deleted()
        user.assertion_is_activated()

        token = user.generate_auth_token(600)
        return {'token': token.decode('ascii'), 'duration': 600}


class Activation(BaseView):

    @RequestValidation.parameters_assertion(parameters=['activation_code'])
    def get(self, **kwargs):
        user = models.User.objects.get(pk=kwargs['user_id'])
        res = user.verify_activation(self.request.args.get('activation_code'))

        return { 'ok': res}

    @auth.login_required
    def post(self):
        user = global_storage.user
        user.assertion_is_not_deleted()
        #TODO resend activation mail
        return {'success':True}

# class Role(BaseView):
#
#     @auth.login_required
#     def post(self, **kwargs):
#         role = kwargs['role']
#         user = global_storage.user
#         user.assertion_is_not_deleted()



