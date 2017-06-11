from mongoengine import *

from Models.GeneralEmbeddedDocuments import Address
from Models.User import User
from Models.Service import Service

import datetime


class Bussiness(Document):

    name = StringField(required=True,max_length=200)
    # settings = DynamicEmbeddedDocument()
    address = Address
    
    owner = ReferenceField(User)
    employees = ListField(ReferenceField(User))
    clients = ListField(ReferenceField(User))

    services = ListField(ReferenceField(Service))

