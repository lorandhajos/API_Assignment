import unittest

import requests

class TestSubscriptions(unittest.TestCase):
    def setUp(self):
        credentials = {"username": "postgres", "password": "example"}
        login_url = "http://localhost/api/v1/login"

        response = requests.post(login_url, json=credentials, headers={'Accept': 'application/json'})

        self.token = response.json().get('refresh_token')

    def test_get_subscriptions(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.post('http://localhost/api/v1/token_refresh', headers=headers)

        self.assertEqual(result.status_code, 200)
