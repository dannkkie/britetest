from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..database_setup import db

class Movie(db.Model):
    """
    
    This is the model class for the Movie object

    """
    id: Mapped[str] = mapped_column(String(10), primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    type: Mapped[str] = mapped_column(String(20), nullable=True)
    poster: Mapped[str] = mapped_column(String(250), nullable=True)

    def __repr__(self):
        """
        Returns a string representation of the Movie object.
        
        """
        return '<Movie %r>' % self.title
    
    def json(self):
        """
        Returns a dictionary representation of the object.

        """
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'type': self.type,
            'poster': self.poster
        }
