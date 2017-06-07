from views import BaseView
from Models.User import User
from Models.Config import Config
from flask import current_app as app

import os


class test(BaseView):
    def get(self):
        self.request.asdf
