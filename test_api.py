import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

from app import create_app
from database.models import setup_db, db_drop_and_create_all, Movie, Actor

# This test will delete all the rows in the db !! only use locally

# Auth tokens
assistant = (
    'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQkRNamN3TkRZNF'
    'FVTTVNemM1TkRBNE9URTBOekJDTnpORVFqbEZPRVExT0RFMk9VVXlNZyJ9.eyJp'
    'c3MiOiJodHRwczovL2ZzbmRxMS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVh'
    'MWM0Y2Q3NDFhMDcwZTBiMmMxMjcwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE'
    '1ODgyNDYwODUsImV4cCI6MTU4ODMzMjQ4NSwiYXpwIjoiclhHeFU0dWRneFl3Z2Z'
    'najlSMEZpeUtUcEVYamdDQ3EiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImd'
    'ldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.AqBVs6KMxBbQagOlAYRPTqd3mCSK6'
    'VoS7IQVGfvCx5HqFxiKjCQ_Awrss8oWFQh2Bxzt-Y765kiltPW4OTsi8thSFi1ve'
    '9Ue5yd3bPttKJqyF5S6JLH6SFqJqr1_tyEfnBqTxUZi9EPu2-xLaOCB6uy3uDa1q'
    'iTDS9TkSqTFGT-_xkkKqUuFFtG35qGm8H_qT4khpYuk0KULQ_MCK5V51r6d2x59I'
    'nHpYjHV0FgS3oOU8XWiC_i2Tz295kfo5rZ5cccOhujtaUQq1Ndiql_SRMN5INehP'
    'yk7QgfHIlE9J3859g07PBRZRV82_qVVTKiZQ5y1GVvKFUJmseb8HV-6Tg'
)

director = (
    'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQkRNamN3'
    'TkRZNFFVTTVNemM1TkRBNE9URTBOekJDTnpORVFqbEZPRVExT0RFMk9VVXlNZyJ'
    '9.eyJpc3MiOiJodHRwczovL2ZzbmRxMS5hdXRoMC5jb20vIiwic3ViIjoiYXV0a'
    'DB8NWVhMWM1MDFmZjcxMTUwZGY5MWMzMmI0IiwiYXVkIjoiY2Fwc3RvbmUiLCJp'
    'YXQiOjE1ODgyNDYxMzgsImV4cCI6MTU4ODMzMjUzOCwiYXpwIjoiclhHeFU0dWR'
    'neFl3Z2ZnajlSMEZpeUtUcEVYamdDQ3EiLCJzY29wZSI6IiIsInBlcm1pc3Npb2'
    '5zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsI'
    'nBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.phR'
    'lQlrzeQIpxVDzYCcLugZhYjvdi92Wzs_TX1hRfIZ6siXZq9F44o90MCdiucoaI0'
    'gLkd7wH48nKGlnEMH-4OJoPEHbxE_yti-5eEUU1g-dPT0mNJmcp3UacsxjtCNK6'
    'etKLpN_3Fo6yntr0C-JFjk6cZ6g0ISpm7GhOx3X_BL2311AkqvJgX5VNKzf8sDV'
    'ifZwG_GPok6jycQgaPvjnIvPHyVr6WOzPIraMO9SYkAioy4dcBWcM2KUZYBqyjG'
    '66OoZ8Tu2G4yB7dh9OIeHNlEY-dv4SpNCpzpkuhXY8ehVQeEW8EeoqcKZLTVpti'
    'rgaBHXdBFUIOq4NPILLTQYJw'
)

producer = (
    'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQkRNamN3'
    'TkRZNFFVTTVNemM1TkRBNE9URTBOekJDTnpORVFqbEZPRVExT0RFMk9VVXlNZy'
    'J9.eyJpc3MiOiJodHRwczovL2ZzbmRxMS5hdXRoMC5jb20vIiwic3ViIjoiYXV'
    '0aDB8NWVhMWM1MjBmZjcxMTUwZGY5MWMzMzFkIiwiYXVkIjoiY2Fwc3RvbmUiL'
    'CJpYXQiOjE1ODgyNDYxOTgsImV4cCI6MTU4ODMzMjU5OCwiYXpwIjoiclhHeFU0'
    'dWRneFl3Z2ZnajlSMEZpeUtUcEVYamdDQ3EiLCJzY29wZSI6IiIsInBlcm1pc3N'
    'pb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG'
    '9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMi'
    'LCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.LbBl0W1SDKSUq-s8VRzIBy'
    'jWI227R2Cm7etEuuEWNwRLEaLdGVAa7tuPWpyR0Lz7QoWjvRqFBVGPYHHSrqLri'
    'MUAeGwhe-S1ANx3ygn599z2KdeYhuSpLAdcGanAxZC69Uu3fsepoz-HwsTFRC4r'
    '8aRgf4x-AVmfAApnRzpm32zeOwf2227U0ZESLp2pzXHq9UK_25x8XLCmdJ1O1ZZ'
    'YQ4eftu1HSgPvCg3W4Mlr7nlToL8etRiSVyi3WZv2mi1zchQivKwdW847-lQMzr'
    '26lUrTI3Wy8vdDpGMxftVljGSK4Ode1RWyj5wbfHxJrhYrUrDKlzrSNXpSGwu81'
    'XRVCA'
)


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = (
            'postgresql://postgres:1111@localhost:5432/casting'
        )
        self.header_assistant = {
            'Content-Type': 'application/json',
            'Authorization': assistant
        }
        self.header_director = {
            'Content-Type': 'application/json',
            'Authorization': director
        }
        self.header_producer = {
            'Content-Type': 'application/json',
            'Authorization': producer
        }
        setup_db(self.app, self.database_path)

    def tearDown(self):
        pass

    def test_0_refresh_db(self):
        db_drop_and_create_all()

    def test_1_get_movies(self):
        # All roles can perform this function
        res = self.client().get('/movies', headers=self.header_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_2_get_actors(self):
        # All roles can perform this function
        res = self.client().get('/actors', headers=self.header_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_3_post_movies(self):
        # Only producer can perform this function
        new_movie = {
            "title": "love actually",
            "release_date": 20200428
        }
        res = self.client().post(
                    '/movies',
                    json=new_movie,
                    headers=self.header_producer
                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_4_post_actors(self):
        # Director and producer can perform this function
        new_actor = {
            "name": "brad pitt",
            "age": 45,
            "gender": "male"
        }
        res = self.client().post(
                    '/actors',
                    json=new_actor,
                    headers=self.header_director
                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_5_patch_movies(self):
        # Director and producer can perform this function
        patch_movie = {
            "title": "love actually",
            "release_date": 20190428
        }
        res = self.client().patch(
                    '/movies/1',
                    json=patch_movie,
                    headers=self.header_director
                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_6_patch_actors(self):
        # Director and producer can perform this function
        patch_actor = {
            "name": "brad pitt",
            "age": 45,
            "gender": "female"
        }
        res = self.client().patch(
                    '/actors/1',
                    json=patch_actor,
                    headers=self.header_director
                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_7_delete_movies(self):
        # Only producer can perform this function
        res = self.client().delete('/movies/1', headers=self.header_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_8_delete_actors(self):
        # Director and producer can perform this function
        res = self.client().delete('/actors/1', headers=self.header_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
