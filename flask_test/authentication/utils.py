import datetime

import jwt
from flask import current_app

from flask_test.utils import convert_datetime_to_timestamp


def generate_jwt_token(user):
    token_validity_limit = 1440

    payload = {
        'iss': 'flask-test',
        'exp': convert_datetime_to_timestamp(datetime.datetime.utcnow() +
                                             datetime.timedelta(minutes=token_validity_limit)),
        'username': user.username,
        'email': user.email
    }

    token = jwt.encode(payload, current_app.config.get('SECRET_KEY'))

    return token.decode("utf-8")
