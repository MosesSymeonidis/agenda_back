from mongoengine import *
import models

class Business(models.base.BaseDocument):

    name = StringField(required=True, max_length=200)
    settings = DictField()

    address = EmbeddedDocumentField(models.Address)

    @property
    def owner(self):
        return models.User.objects(owned_businesses=self).all()

    @property
    def employees(self):
        return models.User.objects(employee__business=self).all()

    @property
    def clients(self):
        return models.User.objects(client__business=self).all()

    @property
    def features(self):
        plans = models.Config.objects.get(config_id='plans')
        return plans['settings'][self.owner.plan]['features']

    @property
    def services(self):
        return models.Service.objects(business=self).all()
