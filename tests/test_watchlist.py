import unittest

import requests

class TestWatchlist(unittest.TestCase):
    def setUp(self):
        credentials = {"username": "postgres", "password": "example"}
        login_url = "http://localhost/api/v1/login"

        response = requests.post(login_url, json=credentials, headers={'Accept': 'application/json'})

        self.token = response.json().get('access_token')

    def test_get_watchlist(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/watchlist', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_get_watchlist_by_id(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/watchlist/1/', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_post_watchlist(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            "name": "example"
        }
        result = requests.post('http://localhost/api/v1/watchlist', headers=headers, json=data)

        self.assertEqual(result.status_code, 200)

    def test_put_watchlist(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            "name": "example"
        }
        result = requests.put('http://localhost/api/v1/watchlist/1/', headers=headers, json=data)

        self.assertEqual(result.status_code, 200)

    def test_delete_watchlist(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.delete('http://localhost/api/v1/watchlist', headers=headers)

        self.assertEqual(result.status_code, 200)
