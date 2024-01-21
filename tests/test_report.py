import unittest

import requests

class TestReport(unittest.TestCase):
    def setUp(self):
        credentials = {"username": "postgres", "password": "example"}
        login_url = "http://localhost/api/v1/login"

        response = requests.post(login_url, json=credentials, headers={'Accept': 'application/json'})

        self.token = response.json().get('access_token')

    def test_get_report_country(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/report/country', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_get_report_films_names(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/report/views_report_films_names', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_get_report_films_views(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/report/views_report_films_views', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_get_report_series_title(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/report/views_report_series_title', headers=headers)

        self.assertEqual(result.status_code, 200)

    def test_get_report_series_views(self):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        result = requests.get('http://localhost/api/v1/report/views_report_series_views', headers=headers)

        self.assertEqual(result.status_code, 200)
