from werkzeug.security import generate_password_hash

from ..database_setup import db
from ..models.user import User


def set_users():
    """
    Sets up the initial users in the database if there are no existing users.

    This function creates an admin user with the username 'admin' and a user
    with the username 'user'. It sets their passwords using the 
    `generate_password_hash` function. The admin user is assigned the role of
    'admin' and the regular user is assigned the role of 'user'. 

    """

    if User.query.first() is None:

        admin = User(username='admin', password_hash=generate_password_hash('admin'), role='admin')

        user = User(username='user', password_hash=generate_password_hash('user'), role='user')

        db.session.add(admin)
        db.session.add(user)
        db.session.commit()