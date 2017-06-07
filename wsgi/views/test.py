from views import BaseView
from Models.Message import Mail
from Models.Config import Config
from flask import current_app as app

import os


class test(BaseView):
    def get(self):
        from flask_mail import Message as FlaskMessage
        msg = FlaskMessage(
            subject='bourda',
            body='yolo',
            sender='moi2113@gmail.com',
            recipients=['msymewnidhs2113@yahoo.gr'])
        app.send(message=msg)
