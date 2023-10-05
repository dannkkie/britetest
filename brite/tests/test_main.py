import unittest
from sqlalchemy import MetaData

from brite import create_app, db

class MovieTestCase(unittest.TestCase):
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

    def test_database_creation(self):
        """
        This function tests the creation of the database by using the `create_all()` 
        method of the `db` object. It creates a new instance of `MetaData` and 
        reflects the database schema using the `bind` argument of the `reflect()` 
        method. It then retrieves all the tables from the reflected metadata and 
        asserts that the `tables` variable is not `None`.

        """
        with self.app.app_context():
            db.create_all()
            meta = MetaData()
            meta.reflect(bind=db.engine)
            tables = meta.tables
            self.assertIsNotNone(tables)


    def test_get_all_movies(self):
        """
        This test case sends a GET request to the '/api/v1/movies' endpoint 
        using the test client.
        It then asserts that the response status code is 200 and that the 
        'movies' attribute in the response JSON is a list.

        """
        response = self.client.get('/api/v1/movies')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['movies'], list)

    def test_get_movie_by_title(self):
        """  
        This function sends a GET request to the 'api/v1/movies/title/{title}' endpoint of the client's API 
        with the specified movie title. It then asserts that the response status code 
        is equal to 200 and that the 'movie' attribute in the response JSON is an instance of a dictionary.

        """
        response = self.client.get('api/v1/movies/title/Batman: The Movie')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['movie'], dict)

    def test_get_movie_by_id(self):
        """
        This function sends a GET request to the 'api/v1/movies/id/{id}' endpoint of the client's API 
        with the specified movie id. It then asserts that the response status code 
        is equal to 200 and that the 'movie' attribute in the response JSON is an instance of a dictionary.

        """
        response = self.client.get('api/v1/movies/id/tt0113198')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['movie'], dict)



if __name__ == '__main__':
    unittest.main()
