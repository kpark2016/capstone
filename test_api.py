import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

from app import create_app
from database.models import setup_db, db_drop_and_create_all, Movie, Actor

# This test will delete all the rows in the db !! only use locally



# Auth tokens
assistant = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQkRNamN3TkRZNFFVTTVNemM1TkRBNE9URTBOekJDTnpORVFqbEZPRVExT0RFMk9VVXlNZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRxMS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMWM0Y2Q3NDFhMDcwZTBiMmMxMjcwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODgyMjI3NzQsImV4cCI6MTU4ODMwOTE3NCwiYXpwIjoiclhHeFU0dWRneFl3Z2ZnajlSMEZpeUtUcEVYamdDQ3EiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.Y_hG90eQVvqDJifuecR65Z8w3LJYME_1xqO8K15wrn6LkqSyq-sExSCwdkmkl7427ZqjGax5h9yYEPG2LnNPE4hQ53vmwlc6VYKwidNggm41u4G2_e1MITvmmxYPV64SkRVu8mQTUpcQ0HxQCPTAFSaAq8yWsLfsTYr1NjmAB4KahYTzOxuLO2WVwF1OHR_uyl3ZCOySdztdA6y7UxLvxeWJoumWJmYq1RGUQlF14F8nU4kcXkfzCaIW9hiJM-nD_UBALGdPB8dVe7vKb8IDp909C79vzFXGS3dMAtHUkXD6MRgN_K0HbKRtOR9HdR-Ze7i7tBoy0X46fw4ZmvqOtQ' 
director = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQkRNamN3TkRZNFFVTTVNemM1TkRBNE9URTBOekJDTnpORVFqbEZPRVExT0RFMk9VVXlNZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRxMS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMWM1MDFmZjcxMTUwZGY5MWMzMmI0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODgyMjI4MjEsImV4cCI6MTU4ODMwOTIyMSwiYXpwIjoiclhHeFU0dWRneFl3Z2ZnajlSMEZpeUtUcEVYamdDQ3EiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.W-Z2PTIyM9hbUvZSRuO4GvTeH8netm146cqXC3fE6uZxcObfkpZCCVsq6XWL5nUz5U8ogD6fnz0H65cHFJ1as95ScUIZrDu6-XENfu7XEiLY4HW2Uk8_2otrwaUmpvuPh9hG23OLKCpYiEFJJ0LbASDn4mvhcFyDVmh127O0RbeWBDeEj6WpJx1cPnpFCVaBjYOMZ8WvF0JoFP2YhQhyqZjOagFoBCcpnO4CqlBuQpWs4omM1SaMXyGkeZEU3kYlMWHoEXXhAwRR_mg81dJv3DqFedxaTXFFGRRzzrf8LKqLsWLWRfyqhvl0pSS4U8Wt5n8XwcQ-uOAumJCW2cfAqg'
producer = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQkRNamN3TkRZNFFVTTVNemM1TkRBNE9URTBOekJDTnpORVFqbEZPRVExT0RFMk9VVXlNZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRxMS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMWM1MjBmZjcxMTUwZGY5MWMzMzFkIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODgyMjI4ODgsImV4cCI6MTU4ODMwOTI4OCwiYXpwIjoiclhHeFU0dWRneFl3Z2ZnajlSMEZpeUtUcEVYamdDQ3EiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.vG-xwG12cK37MxAOeXk22uLU2vaTn9XlNpxg4z8BLAWZUwe8J6jDJ2ye99-G-BJHFPvey-33Fkw9Gs5u0muwe5QyugGksWoxMqzoC5tRo2z3aNLT5P_f3jB322mIfSfFbRQZSgIZymY8dHvqC6m19Dd-edMS4w4PkH-7jRqzftcDtiPQU8pexkK9hHlVEk3tukT7y9-uT7FQ4Fqxrhz1xLZa-f2W4GEZjLQeCcjIoX0CUcGndr5UOvP5L7qJwf3P6f-39AN611PPu79VGaicrIEaOCHYtiyvq3daujjYMfkccYxStSOqtWwlyEiZ1HIbZMfK42J1lz5W1NGWISwa4Q'

class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql://postgres:1111@localhost:5432/casting'
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
            "title":"love actually",
            "release_date":20200428
        }
        res = self.client().post('/movies', json=new_movie, headers=self.header_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_4_post_actors(self):
        # Director and producer can perform this function
        new_actor = {
            "name":"brad pitt",
            "age":45,
            "gender":"male"
        }
        res = self.client().post('/actors', json=new_actor, headers=self.header_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_5_patch_movies(self):
        # Director and producer can perform this function
        patch_movie = {
            "title":"love actually",
            "release_date":20190428
        }
        res = self.client().patch('/movies/1', json=patch_movie, headers=self.header_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_6_patch_actors(self):
        # Director and producer can perform this function
        patch_actor = {
            "name":"brad pitt",
            "age":45,
            "gender":"female"
        }
        res = self.client().patch('/actors/1', json=patch_actor, headers=self.header_director)
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