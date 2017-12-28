import datetime
import random
import string

from flask import current_app as app
from flask import g as global_storage
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash

from utils.exceptions.user import *
import models


class User(models.base.BaseDocument):
    class PersonalInfo(EmbeddedDocument):
        name = StringField(required=True)
        surname = StringField(required=True)
        birthday = DateTimeField(required=True)
        gender = StringField(choices=('male', 'female', 'other'), required=True)
        profile_pic = ImageField()  # TODO check it again for easier way

    class Bio(EmbeddedDocument):
        description = MultiLineStringField()

    class Client(EmbeddedDocument):
        business = ReferenceField(models.Business)
        alias = StringField()  # TODO required=True)
        email = EmailField()
        phone = StringField()
        description = StringField()

    class Employee(EmbeddedDocument):
        business = ReferenceField(models.Business)
        alias = StringField()  # TODO required=True)
        email = EmailField()
        phone = StringField()

    plans = models.Config.objects.get(config_id='plans')

    TYPE_ADMIN = 'admin'
    TYPE_CLIENT = 'client'
    TYPE_EMPLOYEE = 'employee'
    GUEST_ROLE = 'guest'

    PROFESSIONAL_ROLE = 'professional'

    OWNER_ROLE = 'owner'

    username = StringField(max_length=200, required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=200, required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    activated = BooleanField(default=False)
    activated_at = DateTimeField()
    deleted_at = DateTimeField()
    deleted = BooleanField(required=True, default=False)

    roles = ListField(
        StringField(max_length=20, choices=(PROFESSIONAL_ROLE, OWNER_ROLE, GUEST_ROLE)), default=[GUEST_ROLE])

    client = ListField(EmbeddedDocumentField(Client))

    employee = ListField(EmbeddedDocumentField(Employee))

    admin = ListField(ReferenceField(models.Business))

    plan = StringField(choices=plans.distinct, max_length=10)

    personal_info = EmbeddedDocumentField(PersonalInfo)
    bio = EmbeddedDocumentField(Bio)
    address = models.Address

    owned_businesses = ListField(ReferenceField(models.Business))

    random_secret = StringField()
    token = StringField()

    @property
    def is_business_owner(self):
        return len(self.owned_businesses) > 0

    @property
    def permissions(self):
        configs = models.Config.objects.get(config_id='general')
        permissions = []
        for role in self.roles:
            permissions.append(configs['roles'][role]['permissions'])
        return permissions

    def set_admin_business(self, business):
        self.admin.append(business)

    def set_client_business(self, client):
        self.client.append(client)

    def set_employee_business(self, employee):
        self.employee.append(employee)

    def set_owned_business(self, business):
        self.owned_businesses.append(business)

    def set_credentials(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=600):
        self.random_secret = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(15))
        s = Serializer(self.random_secret, expires_in=expiration)
        self.token = s.dumps({'id': str(self.id)}).decode('ascii')
        self.save()
        return self.token

    def generate_activation_code(self, expiration=6000):
        s = Serializer(app.config['ACTIVATION_SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': str(self.id)})

    def marked_as_deleted(self):
        self.deleted = True
        self.deleted_at = datetime.datetime.now()
        self.save()

    def marked_as_active(self):
        self.activated = True
        self.activated_at = datetime.datetime.now()
        self.save()

    def assertion_is_not_deleted(self):
        if not hasattr(self, 'deleted'):
            raise Exception
        if self.deleted:
            raise Exception

    def assertion_is_activated(self):
        if not hasattr(self, 'activated'):
            raise Exception
        if not self.activated:
            raise Exception

    def verify_activation(self, activation_code):
        s = Serializer(app.config['ACTIVATION_SECRET_KEY'])
        try:
            data = s.loads(activation_code)
        except SignatureExpired:
            return False
        except BadSignature:
            return False

        if self.id == data['id']:
            self.marked_as_active()
            return True
        return False

    def business_permissions(self, business):
        permissions = []
        if business in self.admin:
            permissions.append('admin_permissions')

        if business in [business_id['business_id'] for business_id in self.client]:
            permissions.append('client_permissions')

        if business in [business_id['business_id'] for business_id in self.employee]:
            permissions.append('employee_permissions')
        return permissions

    def check_business_permissions(self, permission, business):
        return permission in self.permissions(business)

    def check_permissions(self, permission):
        return permission in self.permissions

    def assertion_of_businesses_num(self):
        if hasattr(self, 'plan') and self.plan is not None:
            if len(self.owned_businesses) >= self.plans['settings'][self.plan]['business_limit']:
                raise MaxBusinessLimit(self.plan)
        else:
            raise UserHasNotPlan()

    def assertion_role(self, role):
        if not self.check_role(role):
            raise RoleError(role)

    def assertion_business_permission(self, permission, business):
        if not self.check_business_permission(permission, business):
            raise Exception

    def assertion_permission(self, permission):
        if not self.check_permission(permission):
            raise Exception

    def set_bio(self, discription):
        self.bio = self.Bio(description=discription)

    def set_personal_info(self, name, surname, birthday, gender):
        self.personal_info = self.PersonalInfo(name=name, surname=surname, birthday=birthday, gender=gender)

    def check_role(self, role):
        return role in self.roles

    @staticmethod
    def verify_auth_token(token):
        try:
            user = User.objects.get(token=token)
        except:
            return None
        try:
            s = Serializer(user.random_secret)
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.objects.get(pk=data['id'])
        return user

    auth = HTTPBasicAuth()

    @staticmethod
    @auth.verify_password
    def verify_password(username_or_token, password):
        # first try to authenticate by token
        user = User.verify_auth_token(username_or_token)
        if not user:
            # try to authenticate with username/password
            user = User.objects.get(email=username_or_token)
            if not user or not user.check_password(password):
                return False
        global_storage.user = user
        return True
