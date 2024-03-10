import unittest

import requests

class TestGenre(unittest.TestCase):
    def setUp(self):
        credentials = {"username": "postgres", "password": "example"}
        login_url = "http://localhost/api/v1/login"

        response = requests.post(login_url, json=credentials, headers={'Accept': 'application/json'})

        self.token = response.json().get('access_token')

    def test_get_genre(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/genre', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_get_genre_by_id(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/genre/1', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_post_genre(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            "name": "example",
            "age_restriction": 18
        }
        result = requests.post('http://localhost/api/v1/genre', headers=headers, json=data)

        self.assertEqual(result.status_code, 200)

    def test_put_genre(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            "genre_id": 1,
            "name": "example",
            "age_restriction": 18
        }
        result = requests.put('http://localhost/api/v1/genre/10', headers=headers, json=data)

        self.assertEqual(result.status_code, 200)

    def test_delete_genre(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.delete('http://localhost/api/v1/genre/10', headers=headers)

        self.assertEqual(result.status_code, 200)
