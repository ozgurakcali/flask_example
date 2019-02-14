from flask import Blueprint, request, current_app, jsonify
from flask_restful import Api, abort, Resource
from marshmallow import ValidationError

from flask_test.authentication.schemas import LoginSchema
from flask_test.authentication.utils import generate_jwt_token
from flask_test.users.schemas import user_schema

authentication_bp = Blueprint('authentication', __name__)
authentication_api = Api(authentication_bp)


class UserLogin(Resource):

    def post(self):
        try:
            # Validate request data
            user = LoginSchema().load(request.json)
        except ValidationError as err:
            current_app.logger.error(err.messages)
            abort(401, message=err.messages)

        # Log the user in
        user_data = user_schema.dump(user)
        user_data['token'] = generate_jwt_token(user)

        return jsonify(user_data)


authentication_api.add_resource(UserLogin, '/login')
