from flask import Blueprint, request
from flask_restful import Api, Resource

from brite.services.auth_service import login_user


auth_bp = Blueprint('auth', __name__)
auth = Api(auth_bp)


class Login(Resource):
    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        return login_user(username, password)


auth.add_resource(Login, '/login')
