import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

from api import create_app
from database.models import setup_db, db_drop_and_create_all, Movie, Actor

# This test will delete all the rows in the db !! only use locally

# Auth tokens
assistant = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQkRNamN3TkRZNFFVTTVNemM1TkRBNE9URTBOekJDTnpORVFqbEZPRVExT0RFMk9VVXlNZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRxMS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMWM0Y2Q3NDFhMDcwZTBiMmMxMjcwIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODgwNjM1OTIsImV4cCI6MTU4ODE0OTk5MiwiYXpwIjoiclhHeFU0dWRneFl3Z2ZnajlSMEZpeUtUcEVYamdDQ3EiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.kNxmr9u1Hv1jJplbFo1TywZlB_mbHKm_z-Gwt5g3WLdF5nUGuQRfwkc4Sjt2Ib9VpKRCZ33vtEXHuaUQutkddU3Ngxy7VRxqTchpN8_tgiOV3CPlzcO-5DBN3JIHbF6FFyAUVceG3-dm9dUFu76ZpP4qXxMz3BLtw68hgxxg_0SfWee03ac9dvw3pTm0AafG_oiD3uwPXWgF2LadNg5naocEDhe_wI5t9OEN2t0vqt35KkhdEcuizpyyfpsJ56KARxcIGAc1Hn5ncsWJGL_DqUsvOSgWNOWOpKCi8prwRo9qQiYhbUI6ZrLwI4SbuPl6e7heLVmHDfiZL27YZy6oOg'
director = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQkRNamN3TkRZNFFVTTVNemM1TkRBNE9URTBOekJDTnpORVFqbEZPRVExT0RFMk9VVXlNZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRxMS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMWM1MDFmZjcxMTUwZGY5MWMzMmI0IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODgwNjM3OTksImV4cCI6MTU4ODE1MDE5OSwiYXpwIjoiclhHeFU0dWRneFl3Z2ZnajlSMEZpeUtUcEVYamdDQ3EiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.GZPCnMR18eiLioHOqVZSGJyh2mejEZfg4fExwocW13bT5xEFh1oiOEbcvZged1FalFDEJBYd7iO8mvYkGpKPxogbGU_LwUQojIRAlYlWhHAMarWM6xzGtYL0-rSNJ8MpMdY9tIOTw5KMiEwxBEP3wT2YSV-IB7xjLbTIzCntg3l4zkX2vqmofVzQx-h8B7wvcca4oWvcgX6K5MTBhlE63ALNt7YsTgQHf0fqoGC83Dk4lMNfF_9OKJXltf98l4ijbqLNANBF_ccFuoTJM3cg8V9CMxVhEnme2LedTHMnuaUWU6CDjA2bh4AQXVWLr0ZOY4A0sT2xO_2HvP2ixckaLw'
producer = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUQkRNamN3TkRZNFFVTTVNemM1TkRBNE9URTBOekJDTnpORVFqbEZPRVExT0RFMk9VVXlNZyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRxMS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhMWM1MjBmZjcxMTUwZGY5MWMzMzFkIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1ODgwNjM4NDcsImV4cCI6MTU4ODE1MDI0NywiYXpwIjoiclhHeFU0dWRneFl3Z2ZnajlSMEZpeUtUcEVYamdDQ3EiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.oTgs9fv_31lL8iHKugc4jmslMK3yT9D8sIibHxN9CP3s52TcGFH5H1KpnLEmB9mXXSkX95OEldVmH87bYMEoqKgbaLRSfh1NI9nMxecW5unqvBvAZzKBT_JvWsUJyecpxay8TZyQYT8epnr_W1fJJiwGaQkXDIOtoo5J3uaY43EtwNEcPt4eYXzAdOWWsPt3stibWFhX8Uv1wqAUVpl1icZTfZFX5YL68i25JFyAvrAhirZLcThzJ-LnflFVbQ5FHLx-WAqlFlV2uzL2mHoGaZ2oqm6Kx0WVZzmXaaiW3zep2vGhPRBUiCaXgEML-u6uGfLMDOHyZtEDLvmgz3x2lA'

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