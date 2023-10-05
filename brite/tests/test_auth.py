import unittest

from brite import create_app, db



class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


    def test_login(self):
        """
        Test the login functionality of the API.

        This function sends a POST request to the '/api/v1/login' endpoint with a JSON payload containing an existing username and password. It then asserts that the response contains an access token and that the status code is 200.

        """
        response = self.client.post('/api/v1/login', json={'username': 'user', 'password': 'user'})
        
        self.assertIn('access_token', response.get_json())
        self.assertEqual(response.status_code, 200)

    def test_login_bad_credentials(self):
        """
        Test the login functionality with bad credentials.

        This function sends a POST request to the '/api/v1/login' endpoint with the 
        provided username and password. It then asserts that the response contains 
        an error message and has a status code of 401.

        """
        response = self.client.post('/api/v1/login', json={'username': 'wrong', 'password': 'wrong'})
        
        # Assert that the response contains an error message
        self.assertEqual(response.get_json(), {'msg': 'Bad username or password'})
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
   