import unittest
from unittest.mock import patch, MagicMock
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash


from brite import db, create_app
from brite.models.user import User
from brite.services.auth_service import login_user


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.app.config['JWT_SECRET_KEY'] = 'super-secret'
        self.jwt = JWTManager(self.app)

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_user(self):
        with self.app.app_context():
            # Create a test user
            username = 'testuser'
            password = 'testpassword'
            role = 'user'
            password_hash = generate_password_hash(password)
            user = User(username=username,
                        password_hash=password_hash, role=role)
            db.session.add(user)
            db.session.commit()

            # Attempt to login
            response = self.client.post(
                '/api/v1/login', json={'username': username, 'password': password})

            # Check the response
            self.assertEqual(response.status_code, 200)
            json_data = response.get_json()
            self.assertIn('access_token', json_data)

    def test_login_user_bad_credentials(self):
        with self.app.app_context():
            # Create a test user
            username = 'testuser'
            password = 'testpassword'
            role = 'user'
            password_hash = generate_password_hash(password)
            user = User(username=username,
                        password_hash=password_hash, role=role)
            db.session.add(user)
            db.session.commit()

            # Attempt to login with bad username
            response = self.client.post(
                '/api/v1/login', json={'username': 'badusername', 'password': password})
            self.assertEqual(response.status_code, 401)
            json_data = response.get_json()
            self.assertEqual(json_data['msg'], 'Bad username or password')

            # Attempt to login with bad password
            response = self.client.post(
                '/api/v1/login', json={'username': username, 'password': 'badpassword'})
            self.assertEqual(response.status_code, 401)
            json_data = response.get_json()
            self.assertEqual(json_data['msg'], 'Bad username or password')


if __name__ == "__main__":
    unittest.main()
