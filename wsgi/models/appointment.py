from mongoengine import *
import datetime
import models


class TimeSlot(Document):
    meta = {'allow_inheritance': True}
    start = DateTimeField(required=True)
    end = DateTimeField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    modified_at = DateTimeField()
    created_by_admin = BooleanField(required=True, default=False)
    deleted_at = DateTimeField()
    deleted = BooleanField(required=True, default=False)
    modified_from = ReferenceField(models.User, required=True)
    history = ListField(DictField())


class Break(TimeSlot):
    pass


class Appointment(TimeSlot):
    DELETED_REASON_NO_SHOW = 'no_show'
    DELETED_REASON_BY_ADMIN = 'by_admin'

    DEVICE_MOBILE = 'mobile'
    DEVICE_DESKTOP = 'desktop'

    employee = ReferenceField(models.User, required=True)
    service = ReferenceField(models.Service, required=True)
    clients = ListField(ReferenceField(models.User), required=True)

    delete_reason = StringField(choices=(DELETED_REASON_BY_ADMIN, DELETED_REASON_NO_SHOW))
    device = StringField(required=True, default=DEVICE_DESKTOP, choices=(DEVICE_MOBILE, DEVICE_DESKTOP))

    @property
    def client(self):
        return self.clients[0]

    @property
    def num_of_clients(self):
        return len(self.clients)
