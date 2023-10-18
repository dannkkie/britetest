import unittest
from unittest.mock import patch, MagicMock
from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request

from werkzeug.security import generate_password_hash, check_password_hash


from brite import db, create_app
from brite.models.user import User
from brite.utils.decorators import admin_required
from brite.utils.generate_id import generate_id
from brite.utils.set_users import set_users


class TestUtils(unittest.TestCase):
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

    def test_generate_id(self):
        # Testing if the generated ID starts with "tt"
        self.assertTrue(generate_id().startswith("tt"))

        # Testing if the generated ID is 8 characters long
        self.assertEqual(len(generate_id()), 9)

        # Testing if the generated ID consists of only digits
        self.assertTrue(generate_id()[2:].isdigit())


if __name__ == "__main__":
    unittest.main()
