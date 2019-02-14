from marshmallow import fields, validates, validates_schema, ValidationError, post_load

from flask_test.schemas import ma
from flask_test.models import db
from flask_test.utils import bcrypt
from flask_test.users.models import User


class LoginSchema(ma.Schema):

    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates('username')
    def validate_username(self, value):
        # A user should exists with provided username
        query = db.session.query(User).filter(User.username == value)
        if not db.session.query(query.exists()).scalar():
            raise ValidationError('no user exists with provided username')

    @validates_schema
    def validate_login(self, data):
        # Get user instance first
        user = User.query.filter_by(username=data.get('username')).first()
        if not bcrypt.check_password_hash(user.password, data.get('password')):
            raise ValidationError('invalid password')

    @post_load
    def make_object(self, data):
        # Return user object with the username
        user = User.query.filter_by(username=data.get('username')).first()
        return user
