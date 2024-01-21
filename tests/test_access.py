import unittest

import requests

class TestProfileAccess(unittest.TestCase):
    def setUp(self):
        credentials = {"username": "postgres", "password": "example"}
        login_url = "http://localhost/api/v1/login"

        response = requests.post(login_url, json=credentials, headers={'Accept': 'application/json'})

        self.token = response.json().get('access_token')

    def test_get_profile_access_film(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/profile/1/access_films/1', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_get_profile_access_series(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/profile/1/access_series/1', headers=headers)

        self.assertEqual(result.status_code, 200)