import unittest

import requests

class TestPreferences(unittest.TestCase):
    def setUp(self):
        credentials = {"username": "postgres", "password": "example"}
        login_url = "http://localhost/api/v1/login"

        response = requests.post(login_url, json=credentials, headers={'Accept': 'application/json'})

        self.token = response.json().get('access_token')

    def test_get_preferences(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/preferences', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_get_preferences_by_id(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/preferences/1/', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_post_preferences(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            "name": "example"
        }
        result = requests.post('http://localhost/api/v1/preferences', headers=headers, json=data)

        self.assertEqual(result.status_code, 200)

    def test_put_preferences(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            "name": "example"
        }
        result = requests.put('http://localhost/api/v1/preferences/1/', headers=headers, json=data)

        self.assertEqual(result.status_code, 200)

    def test_delete_preferences(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.delete('http://localhost/api/v1/preferences', headers=headers)

        self.assertEqual(result.status_code, 200)
