## Run Locally

Clone the project

```bash
  git clone https://github.com/dannkkie/britetest//link-to-project
```

Go to the project directory

```bash
  cd britetest
```

Install dependencies

```bash
  python3 -m install -r brite/requirements.txt
```

Set environment variables

```bash
    export FLASK_APP=brite
```

Initialise DB

```bash
  flask db init
  flask db migrate -m "Any message"
  flask db upgrade
```

Start the server

```bash
  gunicorn -w 1 -b :8000 run:app

  or 
  
  flask run
```



## Running Tests

To run tests, run the following command

```bash
  python3 -m unittest brites/tests/test_min.python3

  python3 -m unittest brites/tests/test_auth
```




## Usage/Examples

Lets assume we are going to use Postman to test,
Enter the endpoint url and its :params

1. GET http://localhost:8000/api/v1/movies
    This will list all movies in the databse.

2. GET http://localhost:8000/api/v1/movies?limit=10&page=3
    This will also list all movies on page 3 and return 10 per page

3. GET http://localhost:8000/api/v1/movies/title/{title}
    This will retrieve a movie by title

4. GET http://localhost:8000/api/v1/movies/id/{id}
    This retreive a movie by id


5. POST http://localhost:8000/api/v1/movies
    This endpoint adds a movie to the database,  it accepts a json  object


6. DELETE http://localhost:8000/api/1/movies/{id}
    This endpoint accepts an id as argument  to delete a movie if the authenticated user has role 'admin'.


7. POST http://localhost:8000/api/v1/login
    Thi endpoint accepts a json object as json and return a jwt token

    After getting a token it can be used to authrize a logged in user to be able to delete a record.