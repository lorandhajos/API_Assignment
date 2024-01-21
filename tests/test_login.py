import unittest

import requests

class TestLogin(unittest.TestCase):
    def test_correct_login(self):
        mock_data = {
            "username": "postgres",
            "password": "example"
        }

        result = requests.post('http://localhost/api/v1/login', json=mock_data, headers={'Accept': 'application/json'})

        self.assertEqual(result.status_code, 200)

    def test_incorrect_login(self):
        mock_data = {
            "username": "wrong",
            "password": "wrong"
        }

        result = requests.post('http://localhost/api/v1/login', json=mock_data, headers={'Accept': 'application/json'})

        self.assertEqual(result.status_code, 401)

    def test_incorrect_login_no_accept_header(self):
        mock_data = {
            "username": "postgres",
            "password": "example"
        }

        result = requests.post('http://localhost/api/v1/login', json=mock_data)

        self.assertEqual(result.status_code, 400)
