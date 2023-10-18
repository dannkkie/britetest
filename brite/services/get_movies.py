import os

import requests
from sqlalchemy.exc import OperationalError

from brite.models.movie import Movie
from brite.utils.database_setup import db


def fetch_movies(page, api_key):
    url = f"http://www.omdbapi.com/?s=movie&page={page}&apikey={api_key}"
    response = requests.get(url)
    return response.json()


def create_movie(item):
    return Movie(
        title=item["Title"],
        year=item["Year"],
        id=item["imdbID"],
        type=item["Type"],
        poster=item["Poster"],
    )


def get_movies():
    try:
        if Movie.query.first() is not None:
            print("Movies already exist in the table.")
            return

        api_key = os.getenv("API_KEY")
        assert api_key is not None, "Set the API_KEY environment variable"

        movies = []
        for page in range(1, 11):
            data = fetch_movies(page, api_key)

            movies += [create_movie(item) for item in data.get("Search", [])]

        db.session.bulk_save_objects(movies or [])
        db.session.commit()

    except OperationalError:
        print("The table does not exist. Please check your database setup.")
