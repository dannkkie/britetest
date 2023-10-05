from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash

from ..models.user import User


auth_bp = Blueprint('auth', __name__)
auth = Api(auth_bp)


class Login(Resource):
    def post(self):
        """
        Handles the HTTP POST request to authenticate a user and generate an access token.

        Returns:
            A dictionary containing an access token if the authentication is successful,
            along with an HTTP status code of 200. If the authentication fails, the
            function returns a dictionary with an error message and an HTTP status code
            of 401.
        """
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            return {"msg": "Bad username or password"}, 401

        access_token = create_access_token(identity=username)
        return {"access_token": access_token}, 200

auth.add_resource(Login, '/login')
