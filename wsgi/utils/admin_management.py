from flask import Response, request
from functools import wraps
import models


def check_admin_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    try:
        res = models.Config.objects.get(config_id='general')['admin']
        return username == res['username'] and password == res['password']
    except Exception:
        raise Exception


def admin_authorization(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_admin_auth(auth.username, auth.password):
            raise Exception
        return f(*args, **kwargs)

    return decorated
