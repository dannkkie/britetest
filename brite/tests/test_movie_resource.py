import unittest
from unittest.mock import patch, MagicMock
from flask_restful import reqparse

from brite import db, create_app


class TestMovieResource(unittest.TestCase):
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

    def test_get_all_movies(self):
        # Try to fetch all movies
        response = self.client.get('/api/v1/movies')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['movies'], list)

    def test_get_all_movies_with_optional_args(self):
        # Try to fetch all movies with page and limit optional arguments
        response = self.client.get('/api/v1/movies?limit=10&page=2')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['movies'], list)

    def test_get_movie_by_title(self):
        # Try to fetch a movie by title that exist
        response = self.client.get('api/v1/movies/title/Batman: The Movie')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['movie'], dict)

    def test_get_movie_by_title_not_exist(self):
        # Try to fetch a movie by title that does not exist
        response = self.client.get('/api/v1/movies/title/The Imaginary Movie')

        # Check that the status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

    def test_get_movie_by_id(self):
        # Try to fetch a movie by id that exist
        response = self.client.get('api/v1/movies/id/tt0113198')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['movie'], dict)

    def test_get_movie_by_id_not_exist(self):
        # Try to fetch a movie by id that does not exist
        response = self.client.get('/api/v1/movies/id/tt0000000')

        # Check that the status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

    def test_add_movie_to_db(self):
        response = self.client.post(
            '/api/v1/movies', json={'title': 'The Shawshank Redemption'})
        self.assertEqual(response.status_code, 201)

        # Get the id of the new movie
        movie_id = response.json['movie']['id']

        # Fetch the new movie from the API
        response = self.client.get(f'/api/v1/movies/id/{movie_id}')
        self.assertEqual(response.status_code, 200)

        # Check that the fetched movie data matches the data we sent
        self.assertEqual(response.json['movie']
                         ['title'], 'The Shawshank Redemption')

    def test_add_existing_movie_to_db(self):
        # Post a new movie to the API
        response = self.client.post(
            '/api/v1/movies', json={'title': 'The Shawshank Redemption'})
        self.assertEqual(response.status_code, 201)

        # Try to post the same movie again
        response = self.client.post(
            '/api/v1/movies', json={'title': 'The Shawshank Redemption'})

        # Check that the status code is 400 (Conflict)
        self.assertEqual(response.status_code, 400)

    def test_delete_movie_by_id_with_authorization(self):
        # Login as an admin user and get the access token
        response = self.client.post(
            '/api/v1/login', json={'username': 'admin', 'password': 'admin'})
        access_token = response.json['access_token']

        # Add a movie to the database
        response = self.client.post(
            '/api/v1/movies', json={'title': 'The Shawshank Redemption'})
        self.assertEqual(response.status_code, 201)

        # Get the ID of the movie we just added
        movie_id = response.json['movie']['id']

        # Delete the movie from the database using the access token
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.delete(
            f'/api/v1/movies/{movie_id}', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_movie_by_id_without_authorization(self):
        # Login as a non-admin user
        response = self.client.post(
            '/api/v1/login', json={'username': 'user', 'password': 'user'})
        access_token = response.json['access_token']

        # Post a new movie to the API
        response = self.client.post(
            '/api/v1/movies', json={'title': 'The Shawshank Redemption'})
        self.assertEqual(response.status_code, 201)

        # Get the movie id
        movie_id = response.json['movie']['id']

        # Try to delete the posted movie using the non-admin access token
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.delete(
            f'/api/v1/movies/{movie_id}', headers=headers)

        # Check that the status code is 403 (Forbidden)
        self.assertEqual(response.status_code, 403)

    def test_delete_nonexistent_movie_by_id_with_authorization(self):
        # Login as an admin
        response = self.client.post(
            '/api/v1/login', json={'username': 'admin', 'password': 'admin'})
        access_token = response.json['access_token']

        # Try to delete a movie that does not exist
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.delete(
            '/api/v1/movies/tt0000000', headers=headers)

        # Check that the status code is 404 (Not Found)
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
