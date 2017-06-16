from mongoengine import *

from Models.GeneralEmbeddedDocuments import Address
from Models.User import User
from Models.Service import Service

import datetime


class Business(Document):

    name = StringField(required=True,max_length=200)
    settings = DictField()

    address = EmbeddedDocumentField(Address)
    plan = StringField()
    
    owner = ReferenceField(User)
    employees = ListField(ReferenceField(User))
    clients = ListField(ReferenceField(User))

    services = ListField(ReferenceField(Service))

