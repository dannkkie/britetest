import unittest
from unittest.mock import patch, MagicMock

from brite import db, create_app
from brite.services.movie_service import delete_movie, fetch_movies, fetch_movie_by_title, fetch_movie_by_id, add_movie


class TestMovieService(unittest.TestCase):
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

    @patch('brite.services.movie_service.Movie')
    def test_fetch_movies(self, mock_movie):
        # Mock the Movie.query.order_by().paginate() call
        mock_paginate = MagicMock()
        mock_paginate.items = [mock_movie, mock_movie]
        mock_order_by = MagicMock()
        mock_order_by.paginate.return_value = mock_paginate
        mock_query = MagicMock()
        mock_query.order_by.return_value = mock_order_by
        mock_movie.query = mock_query

        # Mock the Movie.json() call
        mock_movie.json.return_value = {'id': 1, 'title': 'Test Movie'}

        result = fetch_movies(1, 2)
        expected_result = {'movies': [
            {'id': 1, 'title': 'Test Movie'}, {'id': 1, 'title': 'Test Movie'}]}

        self.assertEqual(result, expected_result)

    @patch('brite.services.movie_service.Movie')
    def test_fetch_movies_no_data(self, mock_movie):
        # Mock the Movie.query.order_by().paginate() call to return no items
        mock_paginate = MagicMock()
        mock_paginate.items = []
        mock_order_by = MagicMock()
        mock_order_by.paginate.return_value = mock_paginate
        mock_query = MagicMock()
        mock_query.order_by.return_value = mock_order_by
        mock_movie.query = mock_query

        result = fetch_movies(1, 2)
        expected_result = {'movies': []}

        self.assertEqual(result, expected_result)

    @patch('brite.services.movie_service.Movie')
    def test_fetch_movie_by_title(self, mock_movie):
        # Mock the Movie.query.filter_by().first() call
        mock_filter_by = MagicMock()
        mock_filter_by.first.return_value = mock_movie
        mock_query = MagicMock()
        mock_query.filter_by.return_value = mock_filter_by
        mock_movie.query = mock_query

        # Mock the Movie.json() call
        mock_movie.json.return_value = {'id': 1, 'title': 'Test Movie'}

        result = fetch_movie_by_title('Test Movie')
        expected_result = {'movie': {'id': 1, 'title': 'Test Movie'}}

        self.assertEqual(result, expected_result)

    @patch('brite.services.movie_service.Movie')
    def test_fetch_movie_by_title_not_found(self, mock_movie):
        # Mock the Movie.query.filter_by().first() call to return None
        mock_filter_by = MagicMock()
        mock_filter_by.first.return_value = None
        mock_query = MagicMock()
        mock_query.filter_by.return_value = mock_filter_by
        mock_movie.query = mock_query

        result = fetch_movie_by_title('Nonexistent Movie')
        expected_result = {
            "message": "Movie with this title does not exist"}, 404

        self.assertEqual(result, expected_result)

    @patch('brite.services.movie_service.Movie')
    def test_fetch_movie_by_id_found(self, mock_movie):
        # Mock the Movie.query.get() call
        mock_query = MagicMock()
        mock_query.get.return_value = mock_movie
        mock_movie.query = mock_query

        # Mock the Movie.json() call
        mock_movie.json.return_value = {'id': 1, 'title': 'Test Movie'}

        result = fetch_movie_by_id(1)
        expected_result = {'movie': {'id': 1, 'title': 'Test Movie'}}

        self.assertEqual(result, expected_result)

    @patch('brite.services.movie_service.Movie')
    def test_fetch_movie_by_id_not_found(self, mock_movie):
        # Mock the Movie.query.get() call to return None
        mock_query = MagicMock()
        mock_query.get.return_value = None
        mock_movie.query = mock_query

        result = fetch_movie_by_id(999)
        expected_result = {"message": "Movie with this id does not exist"}, 404

        self.assertEqual(result, expected_result)

    @patch('brite.services.movie_service.Movie')
    @patch('brite.utils.database_setup.db.session')
    def test_add_movie_new_title(self, mock_db_session, mock_movie):
        # Mock the Movie.query.filter_by().first() call to return None
        mock_filter_by = MagicMock()
        mock_filter_by.first.return_value = None
        mock_query = MagicMock()
        mock_query.filter_by.return_value = mock_filter_by
        mock_movie.query = mock_query

        # Mock the Movie.json() call
        new_movie = MagicMock()
        new_movie.json.return_value = {'id': 1, 'title': 'New Movie'}
        mock_movie.return_value = new_movie

        result = add_movie('New Movie')
        expected_result = {'movie': {'id': 1, 'title': 'New Movie'}}, 201

        self.assertEqual(result, expected_result)

    @patch('brite.services.movie_service.Movie')
    def test_add_movie_existing_title(self, mock_movie):
        # Mock the Movie.query.filter_by().first() call to return a movie
        existing_movie = MagicMock()
        mock_filter_by = MagicMock()
        mock_filter_by.first.return_value = existing_movie
        mock_query = MagicMock()
        mock_query.filter_by.return_value = mock_filter_by
        mock_movie.query = mock_query

        result = add_movie('Existing Movie')
        expected_result = {
            "message": "Movie with this title already exists"}, 400

        self.assertEqual(result, expected_result)

    @patch('brite.services.movie_service.Movie')
    @patch('brite.utils.database_setup.db.session')
    def test_delete_movie_found(self, mock_db_session, mock_movie):
        # Mock the Movie.query.get() call to return a movie
        mock_query = MagicMock()
        mock_query.get.return_value = mock_movie
        mock_movie.query = mock_query

        result = delete_movie(1)
        expected_result = {'message': 'Movie deleted.'}, 200

        self.assertEqual(result, expected_result)

    @patch('brite.services.movie_service.Movie')
    def test_delete_movie_not_found(self, mock_movie):
        # Mock the Movie.query.get() call to return None
        mock_query = MagicMock()
        mock_query.get.return_value = None
        mock_movie.query = mock_query

        result = delete_movie(999)
        expected_result = {'message': 'Movie not found.'}, 404

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
