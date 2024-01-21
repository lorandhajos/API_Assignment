import unittest

import requests

class TestAccount(unittest.TestCase):
    def setUp(self):
        credentials = {"username": "postgres", "password": "example"}
        login_url = "http://localhost/api/v1/login"

        response = requests.post(login_url, json=credentials, headers={'Accept': 'application/json'})

        self.token = response.json().get('access_token')

    def test_get_account(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/account', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_post_account(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            "email": "example@email.com",
            "password": "example",
            "payment_method": "example",
            "blocked": False,
            "login_attempts": 0,
            "last_login": "2021-01-01",
            "subscription_id": 1
        }
        result = requests.post('http://localhost/api/v1/account', headers=headers, json=data)

        self.assertEqual(result.status_code, 200)