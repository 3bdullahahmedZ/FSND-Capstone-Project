
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import Actor, Movie, setup_db

DB_USER = 'postgres'
DB_PASSWORD = '12211221'
DB_NAME_TEST = 'capstoneTest'

Casting_Assistant_token = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjllWnlmZ3Z5MmFqd1J6UjBJeEE1SSJ9.eyJpc3MiOiJodHRwczovL2Rldi0xY3pycmNtby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJjMzMxZDI1YTczMjUxNWRkNmYxZWIyIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY2MDE2MTA2NCwiZXhwIjoxNjYwMTY4MjY0LCJhenAiOiJZeW9SdWxGWHp4NjFoQ3F5enVNRTdId1JZR05pTVY5WCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.iZ2JDm80tz01XX2UtOpeeTfhllQznpGxs4BwYm0hBGGXSZk7LPbGwWQ3djwPqfGiHIUcZFYdTBxae241hPN8NOOnzdvpzSFWo3tKvuuy8nv2km3dfEY3YvyDLVveRCvRwui4OXriSi81XVHVi1b0z-hMFaEncyQWwCS1B6ET--2LCh7Rzz5rXzAy1_eVt7oenwCWd3-Cj4-rY0KBo5ShAMCJslzlCjpbwNFt4jRsaWi0hJJ2t1c5wOJaVIC1L7kUlW58OgmNAcMRt0gREoNFsOC-60HvNoS7pL9rOEUsNN4SI_sVLGEs81_gp1Qp3Qqkq8e-eA4c4mySa9ylvLzxow'}
Casting_Director_token = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjllWnlmZ3Z5MmFqd1J6UjBJeEE1SSJ9.eyJpc3MiOiJodHRwczovL2Rldi0xY3pycmNtby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJjMjdlMGZkNjhmNTMzMDgwNzFkNDk3IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY2MDE2MjA1MiwiZXhwIjoxNjYwMTY5MjUyLCJhenAiOiJZeW9SdWxGWHp4NjFoQ3F5enVNRTdId1JZR05pTVY5WCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.onY7GqS-Vm7oPxDLYmjTJ3WLo74HJlGcMTwG586NNbBsbDtuoiW7-BWUKUUQ7vlOQVq0VirbYGz7qhmENWGsLXc3bkXVxzP_AFjt74PNzTpLZCsgtGNBARt_ttBMQ6fACGynxkQB4xaRYKZy3HMLnfSw7BWQ58DEQUSZtKn8ZpRzAPw6e-r_CFnKPJhRRpsao_8dr3Ka39zhKgEa2jV2fFSC5Bgn_OdYlq1BswHDXruPzc2-OyEuaRQxYDxD18p2eq7TQ3HEkXFxoL_HacGCjzvtm1ihIZcT0VWsW61URnvdtWfjU4FWfES_O3_zfmF-DTfbdHhiVsT96IysSsxYZw'}
Executive_Producer_token = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjllWnlmZ3Z5MmFqd1J6UjBJeEE1SSJ9.eyJpc3MiOiJodHRwczovL2Rldi0xY3pycmNtby51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJmMGY3M2Y1Yzc4YjQ0MTQ1MTg2ZTYyIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTY2MDE2MjM2OCwiZXhwIjoxNjYwMTY5NTY4LCJhenAiOiJZeW9SdWxGWHp4NjFoQ3F5enVNRTdId1JZR05pTVY5WCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.A_ygifu5dz9Ta3pc7VPsR4hbyfk0CqlYZmgJTGlZ_cDOEQ4Z91QKpn26bL4FUDenvSO2kTL3PYKqORb4M7ZTOfO_9foz3zpeVCzY82NJL9nHIphEX0AaUGlgx6YiUxwTjt9kLX1uEGs_EYXbH2x_VdN0BitAbLr31vSH6WR4-zZucZj5RKZkz-Ug-duzUfGh1rtwZBgntCxIt9WwHtL3jBNCvhm1ek_ZV9N_Y6pM31SHLWNqhZY4xwWvhGBJyek5F_alX93og234MCdpVu7tmahm0YqzskvyoX0YwRtLWeMMT4P51Vk4VA6HJCIgNibq_yDBIweA5W7hZaFpjjfCSQ'}


class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@localhost:5432/{}'.format(
            DB_USER, DB_PASSWORD, DB_NAME_TEST)
        setup_db(self.app, self.database_path)
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            actor1 = Actor(name='Brad Pitt', age=58, gender='male')
            actor2 = Actor(name='Angelina Jolie', age=47, gender='female')
            movie = Movie(title='Mr. & Mrs. Smith',
                          release_date='June 7, 2005')
            self.db.session.add(actor1)
            self.db.session.add(actor2)
            self.db.session.add(movie)
            movie.cast.append(actor1)
            movie.cast.append(actor2)
            self.db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            self.db.drop_all()

    def test_get_actors(self):
        res = self.client().get("/actors", headers=Executive_Producer_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_movies(self):
        res = self.client().get("/movies", headers=Executive_Producer_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_create_movie(self):
        res = self.client().post("/movies", json={
            'title': 'Toy story',
            'release_date': '10/03/2000',
            'cast': [1, 2],
        }, headers=Executive_Producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_movie_422_missing_arg(self):
        res = self.client().post("/movies", json={
            'release_date': '10/03/2000',
            'cast': [1, 2],
        }, headers=Executive_Producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    def test_create_actor(self):
        res = self.client().post("/actors", json={
            'name': 'jon travolta',
            'gender': 'male',
            'age': 60,
        }, headers=Executive_Producer_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actor']))

    def test_create_actor_422_missing_arg(self):
        res = self.client().post("/actors", json={
            'gender': 'male',
            'age': 60,
        }, headers=Executive_Producer_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)

    def test_modify_movie(self):
        res = self.client().patch("/movies/3", json={
            'title': 'Toy story 3',
        }, headers=Executive_Producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_modify_movie_404(self):
        res = self.client().patch("/movies/1000", json={
            'title': 'Toy story 3',
        }, headers=Executive_Producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_modify_actor(self):
        res = self.client().patch("/actors/3", json={
            'name': 'Nasser',
        }, headers=Executive_Producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_modify_actor_404(self):
        res = self.client().patch("/actors/1000", json={
            'name': 'Nasser',
        }, headers=Executive_Producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_delete_actor(self):
        res = self.client().delete("/actors/1", headers=Executive_Producer_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_delete_actor_404(self):
        res = self.client().delete("/actors/10000", headers=Executive_Producer_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_delete_movie(self):
        res = self.client().delete("/movies/1", headers=Executive_Producer_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    def test_delete_movie_404(self):
        res = self.client().delete("/movies/10000", headers=Executive_Producer_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_casting_assistant(self):
        res = self.client().get("/actors", headers=Casting_Assistant_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_casting_assistant_not_auth(self):
        res = res = self.client().post("/movies", json={
            'title': 'Toy story',
            'release_date': '10/03/2000',
            'cast': [1, 2], }, headers=Casting_Assistant_token)
        self.assertEqual(res.status_code, 403)

    def test_casting_director(self):
        res = self.client().post("/actors", json={
            'name': 'jon travolta',
            'gender': 'male',
            'age': 60,
        }, headers=Casting_Director_token)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_casting_director_not_auth(self):
        res = res = self.client().post("/movies", json={
            'title': 'Toy story',
            'release_date': '10/03/2000',
            'cast': [1, 2], }, headers=Casting_Director_token)
        self.assertEqual(res.status_code, 403)

    def test_exec_producer(self):
        res = res = self.client().post("/movies", json={
            'title': 'Toy story',
            'release_date': '10/03/2000',
            'cast': [1, 2], }, headers=Executive_Producer_token)
        self.assertEqual(res.status_code, 200)

    def test_exec_producer(self):
        res = res = self.client().post("/movies", json={
            'title': 'Toy story',
            'release_date': '10/03/2000',
            'cast': [1, 2], })
        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()
