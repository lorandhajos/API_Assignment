import unittest

import requests

class TestSeries(unittest.TestCase):
    def setUp(self):
        credentials = {"username": "postgres", "password": "example"}
        login_url = "http://localhost/api/v1/login"

        response = requests.post(login_url, json=credentials, headers={'Accept': 'application/json'})

        self.token = response.json().get('access_token')

    def test_get_series(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/series', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_get_series_by_id(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/series/1/', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_post_series(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            "name": "example"
        }
        result = requests.post('http://localhost/api/v1/series', headers=headers, json=data)

        self.assertEqual(result.status_code, 200)

    def test_put_series(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            "name": "example"
        }
        result = requests.put('http://localhost/api/v1/series/1/', headers=headers, json=data)

        self.assertEqual(result.status_code, 200)

    def test_delete_series(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.delete('http://localhost/api/v1/series', headers=headers)

        self.assertEqual(result.status_code, 200)
