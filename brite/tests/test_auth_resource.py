import unittest

from brite import db, create_app


class TestYourResource(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login(self):
        # Try to login with the new user's credentials
        response = self.client.post(
            '/api/v1/login', json={'username': 'user', 'password': 'user'})

        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that an access token is returned
        self.assertIn('access_token', response.json)

    def test_login_nonexistent_user(self):
        # Try to login with a nonexistent user's credentials
        response = self.client.post(
            '/api/v1/login', json={'username': 'nonexistentuser', 'password': 'testpass'})

        # Check that the status code is 401 (Unauthorized)
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
