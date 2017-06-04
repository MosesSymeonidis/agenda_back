from views import BaseView
from Models.User import User
from Models.Config import Config
from flask import current_app as app

import os


class test(BaseView):
    def get(self):
        print ("adsfadfasfasdfa")
        user = User.objects.get(pk="5916c4e544a7211eed4de9b2")
        return user.generate_activation_code()
