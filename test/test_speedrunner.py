import os
import unittest
import json
import flask
from flask import jsonify, request, Response

from speedrunner_server import app, database_path
import speedrunner_consts as consts
import speedrunner_db as db


class TestServer(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()

        database_path = consts.TEST_DATABASE_PATH

        db.clear_db(database_path)
        db.create_tables(database_path)
        db.init_from_csv(consts.TEST_SEED_DATA_PATH, database_path)

        self.assertEqual(app.debug, True)
        
    def tearDown(self):
        pass

    #GET requests
    def test_home(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_get_game_categories(self):
        response = self.app.get('/games/categories/Game_1', follow_redirects=True)
        response_json = json.loads(response.data.decode("utf-8"))
        
        self.assertIn('Cat_1', response_json)
        self.assertIn('Cat_2', response_json)

    def test_get_games(self):
        response = self.app.get('/games/titles/all', follow_redirects=True)
        response_json = json.loads(response.data.decode("utf-8"))

        self.assertIn('Game_1', response_json)
        self.assertIn('Game_2', response_json)
        self.assertIn('Game_3', response_json)
        
    def test_get_players(self):
        response = self.app.get('/players/all', follow_redirects=True)
        response_json = json.loads(response.data.decode("utf-8"))
        
        self.assertIn('Player_1', response_json)
        self.assertIn('Player_2', response_json)
        self.assertIn('Player_3', response_json)
        self.assertIn('Player_4', response_json)
        self.assertIn('Player_5', response_json)
        self.assertIn('Player_6', response_json)

    #POST tests
    def test_add_game(self):
        response = self.app.post('/games/add/', follow_redirects=True, json={'game_title': 'Game_12'})
        self.assertEqual(response.data, b'<p>Successfully added game </p>')

if __name__ == "__main__":
    unittest.main()