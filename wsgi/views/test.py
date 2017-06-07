from views import BaseView
from Models.Message import Mail
from Models.Config import Config
from flask import current_app as app

import os


class test(BaseView):
    def get(self):
        from flask_mail import Message as FlaskMessage
        from flask_mail import Mail
        msg = FlaskMessage(
            subject='bourda',
            body='yolo',
            sender='flaskproject2113@gmail.com',
            recipients=['msymewnidhs2113@yahoo.gr'])
        mail = Mail()
        mail.send(message=msg)
