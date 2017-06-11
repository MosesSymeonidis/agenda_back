from views import BaseView
from Models.Message import Mail
from Models.Config import Config
from flask import current_app as app
from flask_mongoengine import pagination
from Models.User import User
from Utils.Exceptions.Bussiness import NotProperField
import os


class test(BaseView):
    def get(self):
        # from flask_mail import Message as FlaskMessage
        # from flask_mail import Mail
        # msg = FlaskMessage(
        #     subject='bourda',
        #     body='yolo',
        #     sender='cheapbookdev@hotmail.com',
        #     recipients=['msymewnidhs2113@yahoo.gr'])
        # mail = Mail()
        # mail.send(message=msg)
        # raise NotProperField(field_name='asdf')
        return User.objects.skip(1).limit(2).fields(id=1,username=1)
