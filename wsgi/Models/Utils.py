from mongoengine import *
import datetime

class Config(DynamicDocument):
    pass

class Traffic(DynamicDocument):
    created_at = DateTimeField(default=datetime.datetime.now)
