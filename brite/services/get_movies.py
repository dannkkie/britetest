import os
import requests

from ..database_setup import db
from ..models.movie import Movie

def get_movies():
    """
    Retrieves a list of movies from an external API and stores them in the database.

    This function makes a request to the OMDB API to retrieve a list of movies. It
    uses a loop to paginate through the API's results and retrieves movies from
    multiple pages. Each movie is then added to the database using the SQLAlchemy
    ORM. Finally, the changes are committed to the database. The request is done once if the db is empty

    """

    if Movie.query.first() is None:
        api_key = os.getenv('API_KEY')
        if api_key is None:
            print("Set the API_KEY environment variable")
            return

        movies = []
        for i in range(1, 11):
            url = f'http://www.omdbapi.com/?s=movie&page={i}&apikey={api_key}'
            response = requests.get(url)
            data = response.json()

            if 'Search' in data:
                for item in data['Search']:
                    movie = Movie(
                        title=item['Title'],
                        year=item['Year'],
                        id=item['imdbID'],
                        type=item['Type'],
                        poster=item['Poster']
                    )
                    movies.append(movie)

        if movies:
            db.session.bulk_save_objects(movies)
        db.session.commit()
