from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from brite.models.user import User


def login_user(username, password):
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return {"msg": "Bad username or password"}, 401

    access_token = create_access_token(identity=username)
    return {"access_token": access_token}, 200
