import unittest

import requests

class TestProfile(unittest.TestCase):
    def setUp(self):
        credentials = {"username": "postgres", "password": "example"}
        login_url = "http://localhost/api/v1/login"

        response = requests.post(login_url, json=credentials, headers={'Accept': 'application/json'})

        self.token = response.json().get('access_token')

    def test_get_profile(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/profile', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_get_profile_by_id(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/profile/1', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_post_profile(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            "account_id": 5,
            "age": 0,
            "history_id": 7,
            "language": "string",
            "profile_child": True,
            "profile_image": "string",
            "watchlist_id": 7,
            "country": "string",
            "is_trial": True,
            "is_discount": True
        }
        result = requests.post('http://localhost/api/v1/profile', headers=headers, json=data)

        self.assertEqual(result.status_code, 201)

    def test_put_profile(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            "account_id": 1,
            "age": 0,
            "history_id": 0,
            "language": "string",
            "profile_child": True,
            "profile_image": "string",
            "watchlist_id": 0,
            "country": "string",
            "is_trial": True,
            "is_discount": True
        }
        result = requests.put('http://localhost/api/v1/profile/1', headers=headers, json=data)

        self.assertEqual(result.status_code, 200)

    def test_delete_profile(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.delete('http://localhost/api/v1/profile/1', headers=headers)

        self.assertEqual(result.status_code, 200)
