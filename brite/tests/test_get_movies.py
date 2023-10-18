import os
import unittest
from unittest.mock import MagicMock, patch

import requests
from sqlalchemy.exc import OperationalError

from brite import create_app, db
from brite.models.movie import Movie
from brite.services.get_movies import create_movie, fetch_movies, get_movies


class TestGetMovies(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["TESTING"] = True

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    @patch("requests.get")
    @patch("brite.models.movie.Movie.query")
    @patch("brite.db.session")
    def test_get_movies(self, mock_db, mock_query, mock_get):
        # Mock the first() method to return None
        mock_query.first.return_value = None

        # Mock the API response
        mock_get.return_value.json.return_value = {
            "Search": [
                {
                    "Title": "Test Movie",
                    "Year": "2023",
                    "imdbID": "tt1234567",
                    "Type": "movie",
                    "Poster": "https://test.com/poster.jpg",
                }
            ]
        }

        # Call the function
        get_movies()

        # Assert that bulk_save_objects was called with a list of Movie objects
        self.assertEqual(mock_db.bulk_save_objects.call_count, 1)
        args, _ = mock_db.bulk_save_objects.call_args
        self.assertIsInstance(args[0], list)
        self.assertIsInstance(args[0][0], Movie)

    @patch("requests.get")
    def test_fetch_movies(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"Search": []}
        mock_get.return_value = mock_response

        result = fetch_movies(1, "api_key")
        self.assertEqual(result, {"Search": []})

    @patch("requests.get")
    def test_fetch_movies_empty_api_key(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"Search": []}
        mock_get.return_value = mock_response

        result = fetch_movies(1, "")
        self.assertEqual(result, {"Search": []})

    def test_create_movie(self):
        item = {
            "Title": "Test Movie",
            "Year": "2023",
            "imdbID": "tt1234567",
            "Type": "movie",
            "Poster": "https://example.com/poster.jpg",
        }
        movie = create_movie(item)
        self.assertEqual(movie.title, "Test Movie")
        self.assertEqual(movie.year, "2023")
        self.assertEqual(movie.id, "tt1234567")
        self.assertEqual(movie.type, "movie")
        self.assertEqual(movie.poster, "https://example.com/poster.jpg")

    @patch("brite.models.movie.Movie.query")
    @patch("brite.db.session")
    @patch("requests.get")
    def test_get_movies_no_table(self, mock_get, mock_db, mock_query):
        # Mock the first() method to raise an OperationalError
        mock_query.first.side_effect = OperationalError(
            None, None, "The table does not exist. Please check your database setup."
        )

        # Mock the get() method to return a successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"Search": []}

        # Call the function and capture the output
        with patch("builtins.print") as mock_print:
            get_movies()

        # Assert that a message was printed about the missing table
        mock_print.assert_called_once_with(
            "The table does not exist. Please check your database setup."
        )


if __name__ == "__main__":
    unittest.main()
