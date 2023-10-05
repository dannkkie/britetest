from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required

from ..database_setup import db
from ..utils.decorators import admin_required
from ..utils.generate_id import generate_id
from ..models.movie import Movie


main_bp = Blueprint('main', __name__)
main = Api(main_bp)

class GetMovies(Resource):
    def get(self):
        """
        Retrieves a list of movies with pagination.

        Returns:
            dict: A dictionary containing a list of movies. Each movie is represented as a dictionary.

        """

        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int, help='Number of records to return', default=10, location='args')
        parser.add_argument('page', type=int, help='Page number', default=1, location='args')
        args = parser.parse_args()

        pagination = Movie.query.order_by(Movie.title).paginate(page=args['page'], per_page=args['limit'], error_out=False)

        movies = pagination.items
        return {'movies':[movie.json() for movie in movies]}
    
class GetMovie(Resource):
    def get(self, movie_title=None, movie_id=None):
        """
        Retrieves a movie by title or id.

        Returns:
            dict: A dictionary containing a movie object. Each movie is represented as a dictionary.

        """

        if movie_title:
            movie = Movie.query.filter_by(title=movie_title).first()
            if movie is None:
                return {"message": "Movie with this title does not exist"}, 404
        elif movie_id:
            movie = Movie.query.get(movie_id)
            if movie is None:
                return {"message": "Movie with this id does not exist"}, 404
        else:
            return {"message": "No movie title or id provided"}, 400

        return {'movie': movie.json()}

    

class AddMovie(Resource):
        
    def post(self):
        """
        Creates a new movie record in the database.

        Returns:
            A dictionary containing the newly created movie object and the HTTP status code 201.

        """
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Movie title provided', location='json')
        args = parser.parse_args()

        title = args['title']
        movie = Movie.query.filter_by(title=title).first()

        if movie is not None:
            return {"message": "Movie with this title already exists"}, 400

        code = generate_id()
        movie = Movie(id=code, title=title)
        db.session.add(movie)
        db.session.commit()

        return {'movie': movie.json()}, 201


class DeleteMovie(Resource):

    @jwt_required()
    @admin_required
    def delete(self, movie_id):
        """
        Delete a movie from the database by its identifier.

        Parameters:
            identifier (str): The identifier of the movie to be deleted.

        Returns:
            dict: A dictionary containing the message 'Movie deleted.' if the movie was found and deleted successfully.
                  A dictionary containing the message 'Movie not found.' if the movie was not found in the database.

        """

        movie = Movie.query.get(movie_id)

        if movie:
            db.session.delete(movie)
            db.session.commit()
            return {'message': 'Movie deleted.'}, 200
        else:
            return {'message': 'Movie not found.'}, 404

        
main.add_resource(GetMovies, '/movies')
main.add_resource(GetMovie, '/movies/title/<string:movie_title>', '/movies/id/<string:movie_id>')
main.add_resource(AddMovie, '/movies')
main.add_resource(DeleteMovie, '/movies/<string:movie_id>')
