from mongoengine import *

from Models.GeneralEmbeddedDocuments import Address
from Models.Utils import Config


class Business(Document):
    name = StringField(required=True, max_length=200)
    settings = DictField()

    address = EmbeddedDocumentField(Address)

    @property
    def owner(self):
        from Models.User import User
        return User.objects(owned_businesses=self).all()

    @property
    def employees(self):
        from Models.User import User
        return User.objects(employee__business=self).all()

    @property
    def clients(self):
        from Models.User import User
        return User.objects(client__business=self).all()

    @property
    def features(self):
        plans = Config.objects.get(config_id='plans')
        return plans['settings'][self.owner.plan]['features']

    @property
    def services(self):
        from Models.Service import Service
        return Service.objects(business=self).all()
