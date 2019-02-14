#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

import jwt
from flask import Flask, request, g
from flask_migrate import Migrate
from jwt import DecodeError, ExpiredSignatureError

from flask_test.authentication.views import authentication_bp
from flask_test.models import db
from flask_test.schemas import ma
from flask_test.users.models import User
from flask_test.users.views import users_bp
from flask_test.utils import bcrypt


# Initialize migration manager
migrate = Migrate()


def create_app(config_name=None):
    app = Flask(__name__)

    # If environment not passed, try to read it from environment
    if not config_name:
        config_name = os.environ.get('FLASK_ENV', 'development')

    # Configure application
    app.config.from_object('flask_test.config.{}'.format(config_name.capitalize()))

    # Registering blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(authentication_bp)

    # Database initialization
    db.init_app(app)
    db.app = app

    # Set migration manager configuration
    migrate.init_app(app, db)

    # Schema initialization
    ma.init_app(app)

    # Initialize crypto utility
    bcrypt.init_app(app)

    @app.before_request
    def check_auth_token():
        """
        Check Authorization token before each request, and set user in context accordingly
        """
        auth_header = request.headers.environ.get('HTTP_AUTHORIZATION', None)
        if auth_header:
            token_type, token_value = auth_header.split(' ')

            try:
                payload = jwt.decode(jwt=token_value, key=app.config.get('SECRET_KEY'))
            except DecodeError:
                # Decode failed, invalid token or not signed with our secret
                g.user = None
            except ExpiredSignatureError:
                # Token expired
                g.user = None
            else:
                # Find user in the token and set it in context
                user = User.query.filter_by(username=payload.get('username')).first()
                g.user = user
        else:
            g.user = None

    return app
