from marshmallow import validates, ValidationError, fields, validates_schema

from flask_test.users.models import User
from flask_test.models import db
from flask_test.schemas import ma


class UserSchema(ma.ModelSchema):

    password_confirm = fields.Str(required=True)

    class Meta:
        model = User

    @validates('username')
    def validate_username(self, value):
        # Username should be unique
        query = db.session.query(User).filter(User.username == value)
        if db.session.query(query.exists()).scalar():
            raise ValidationError('username must be unique')

    @validates_schema
    def validate_user(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise ValidationError('passwords must match')


user_schema = UserSchema(exclude=['password'])
users_schema = UserSchema(exclude=['password'], many=True)
