from functools import wraps

from flask import g
from flask_restful import abort


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            abort(401, message='you do not have authorization to access this resource')

        return f(*args, **kwargs)

    return decorated_function
