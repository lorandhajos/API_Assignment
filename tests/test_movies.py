import unittest

import requests

class TestMovies(unittest.TestCase):
    def setUp(self):
        credentials = {"username": "postgres", "password": "example"}
        login_url = "http://localhost/api/v1/login"

        response = requests.post(login_url, json=credentials, headers={'Accept': 'application/json'})

        self.token = response.json().get('access_token')

    def test_get_movies(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/movies', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_get_movies_by_id(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/movies/1', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_post_movies(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            "id": 1,
            "tile": "example",
            "duration": 1
        }
        result = requests.post('http://localhost/api/v1/movies', headers=headers, json=data)

        self.assertEqual(result.status_code, 201)

    def test_put_movies(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            "id": 1,
            "title": "example",
            "duration": 1
        }
        result = requests.put('http://localhost/api/v1/movies/1', headers=headers, json=data)

        self.assertEqual(result.status_code, 200)

    def test_delete_movies(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.delete('http://localhost/api/v1/movies/1', headers=headers)

        self.assertEqual(result.status_code, 200)
