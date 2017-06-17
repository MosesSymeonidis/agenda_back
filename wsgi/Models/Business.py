from mongoengine import *

from Models.GeneralEmbeddedDocuments import Address
from Models.User import User
from Models.Service import Service
from Models.Utils import Config

import datetime


class Business(Document):

    name = StringField(required=True,max_length=200)
    settings = DictField()

    address = EmbeddedDocumentField(Address)

    owner = ReferenceField(User, required=True)
    employees = ListField(ReferenceField(User))
    clients = ListField(ReferenceField(User))

    services = ListField(ReferenceField(Service))

    @property
    def features(self):
        plans = Config.objects.get(config_id='plans')
        return plans['settings'][self.owner.plan]['features']

