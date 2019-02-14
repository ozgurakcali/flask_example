from flask import request, current_app, Blueprint
from flask_restful import Resource, abort, Api
from marshmallow import ValidationError

from flask_test.authentication.decorators import login_required
from flask_test.models import db
from flask_test.users.models import User
from flask_test.users.schemas import UserSchema, users_schema, user_schema

users_bp = Blueprint('users', __name__)
users_api = Api(users_bp)


class Users(Resource):
    """
    Resource responsible for user operations
    """

    @login_required
    def get(self):
        all_users = User.query.all()
        return users_schema.dump(all_users)

    def post(self):
        try:
            # Validate request data
            user = UserSchema().load(request.json)
        except ValidationError as err:
            current_app.logger.error(err.messages)
            abort(400, message=err.messages)

        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user), 201


users_api.add_resource(Users, '/users')
