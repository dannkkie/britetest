from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..utils.database_setup import db


class User(db.Model):
    """

    This is the model class for the Movie object

    Parameters:
        id: id of the user
        username: The username of the user
        password_hash: hash of the user password
        role: role of the user either an admin or user

    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128))
    role: Mapped[str] = mapped_column(String(80), nullable=False)

    def __repr__(self):
        """
        Return a string representation of the User object.

        """
        return "<User %r>" % self.username

    def json(self):
        """
        Returns a dictionary representation of the object.

        """
        return {
            "id": self.id,
            "username": self.username,
        }
