from brite.models.movie import Movie
from brite.utils.database_setup import db
from brite.utils.generate_id import generate_id


def fetch_movies(page: int, limit: int):
    pagination = Movie.query.order_by(Movie.title).paginate(
        page=page, per_page=limit, error_out=False
    )
    movies = pagination.items
    return {"movies": [movie.json() for movie in movies]}


def fetch_movie_by_title(movie_title):
    movie = Movie.query.filter_by(title=movie_title).first()
    if movie is None:
        return {"message": "Movie with this title does not exist"}, 404
    return {"movie": movie.json()}


def fetch_movie_by_id(movie_id):
    movie = Movie.query.get(movie_id)
    if movie is None:
        return {"message": "Movie with this id does not exist"}, 404
    return {"movie": movie.json()}


def add_movie(movie_title):
    movie = Movie.query.filter_by(title=movie_title).first()

    if movie is not None:
        return {"message": "Movie with this title already exists"}, 400

    code = generate_id()
    movie = Movie(id=code, title=movie_title)
    db.session.add(movie)
    db.session.commit()

    return {"movie": movie.json()}, 201


def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)

    if movie:
        db.session.delete(movie)
        db.session.commit()
        return {"message": "Movie deleted."}, 200
    else:
        return {"message": "Movie not found."}, 404
