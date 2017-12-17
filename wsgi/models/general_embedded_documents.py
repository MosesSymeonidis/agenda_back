from mongoengine import *


class Address(EmbeddedDocument):

    country = StringField()
    area = StringField()
    city = StringField()
    street = StringField()
    number = IntField()
    # geolocation = PointField()
