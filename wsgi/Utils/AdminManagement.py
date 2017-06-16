from flask import Response, request
from functools import wraps
from Models.Utils import Config


def check_admin_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    try:
        res = Config.objects.get(config_id='general')['admin']
        return username == res['username'] and password == res['password']
    except Exception:
        return False

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def admin_authorization(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_admin_auth(auth.username, auth.password):
            return {'success':False}
        return f(*args, **kwargs)
    return decorated