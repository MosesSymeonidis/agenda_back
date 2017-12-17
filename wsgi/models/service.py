from mongoengine import *
from flask import current_app as app
import models

class Service(Document):
    schema = models.Config.objects.get(config_id='schema')
    # from Models import User as model_user_at_service
    name = StringField(required=True, max_length=200)

    official_name = StringField(required=True, max_length=200)
    type = StringField(required=True, choices=schema['categories'].keys())
    tags = ListField(StringField(max_length=200))

    duration = FloatField(required=True, choices=schema['services']['duration'])
    employees = ListField(ReferenceField(models.User))
    max_clients = IntField(min_value=1, default=1, required=True)
    #
    bussiness = ReferenceField(models.Business)

    #TODO check again this
    def save(self, force_insert=False, validate=True, clean=True,
             write_concern=None, cascade=None, cascade_kwargs=None,
             _refs=None, save_condition=None, signal_kwargs=None, **kwargs):


        official_name = self.official_name
        services = schema['categories'][self.type]['services']
        for service in services:
            if service['name'] == official_name:
                for tag in self.tags:
                    if tag not in service['possible_tags']:
                        raise InvalidDocumentError()

        return super(Document, self).save(force_insert=False, validate=True, clean=True,
             write_concern=None, cascade=None, cascade_kwargs=None,
             _refs=None, save_condition=None, signal_kwargs=None, **kwargs)



