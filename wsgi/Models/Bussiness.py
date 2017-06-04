from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask import current_app as app
from flask import g as global_storage
from Models.GeneralEmbeddedDocuments import Address
from Models.User import User

import datetime






class Bussiness(Document):

    name = StringField(required=True,max_length=200)
    settings = DynamicEmbeddedDocument()
    address = EmbeddedDocument(Address)
    
    owner = ReferenceField(User)
    employees = ListField(ReferenceField(User))
    clients = ListField(ReferenceField(User))

