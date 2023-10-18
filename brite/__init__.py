import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager

from .resources.auth import auth_bp
from .resources.movie import main_bp
from .services.get_movies import get_movies
from .utils.database_setup import db, migrate
from .utils.set_users import set_users

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)

    @jwt.invalid_token_loader
    def invalid_token_callback(invalid_token):
        return {"message": "Invalid token!"}, 422

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {"message": "Missing token!"}, 401

    with app.app_context():
        db.create_all()
        get_movies()
        set_users()

    app.register_blueprint(auth_bp, url_prefix="/api/v1")
    app.register_blueprint(main_bp, url_prefix="/api/v1")

    return app
