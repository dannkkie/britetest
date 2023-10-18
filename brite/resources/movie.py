from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Api, Resource, reqparse

from brite.services.movie_service import (
    add_movie,
    delete_movie,
    fetch_movie_by_id,
    fetch_movie_by_title,
    fetch_movies,
)
from brite.utils.decorators import admin_required

main_bp = Blueprint("main", __name__)
main = Api(main_bp)


class GetMovies(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "limit",
            type=int,
            help="Number of records to return",
            default=10,
            location="args",
        )
        parser.add_argument(
            "page", type=int, help="Page number", default=1, location="args"
        )
        args = parser.parse_args()

        return fetch_movies(args["page"], args["limit"])


class GetMovieByTitle(Resource):
    def get(self, movie_title):
        return fetch_movie_by_title(movie_title)


class GetMovieById(Resource):
    def get(self, movie_id):
        return fetch_movie_by_id(movie_id)


class AddMovie(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "title",
            type=str,
            required=True,
            help="Movie title provided",
            location="json",
        )
        args = parser.parse_args()

        return add_movie(args["title"])


class DeleteMovie(Resource):
    @jwt_required()
    @admin_required
    def delete(self, movie_id):
        return delete_movie(movie_id)


main.add_resource(GetMovies, "/movies")
main.add_resource(GetMovieByTitle, "/movies/title/<string:movie_title>")
main.add_resource(GetMovieById, "/movies/id/<string:movie_id>")
main.add_resource(AddMovie, "/movies")
main.add_resource(DeleteMovie, "/movies/<string:movie_id>")
