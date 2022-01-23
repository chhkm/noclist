import unittest
from unittest import mock

import requests
import responses

from noclist import formatted, get_auth_token, get_checksum, get_users, retry

BASE_URL = 'http://0.0.0.0:8888'

class TestNoclist(unittest.TestCase):

    @responses.activate
    @mock.patch('noclist.retry')
    def test_get_auth_token(self, mock_retry):
        """Tests get_auth_token()"""
        responses.add(
            responses.GET,
            url=BASE_URL + '/auth',
            status=200
        )

        response = requests.Response()
        response.status_code = 200
        response.headers = {'Badsec-Authentication-Token': '12345'}

        mock_retry.return_value = response
        auth_token = get_auth_token()
        assert auth_token == '12345'


    def test_get_checksum(self):
        """Tests get_checksum()"""
        auth_token = '12345'
        endpoint = '/users'
        checksum = get_checksum(auth_token, endpoint)
        assert checksum == 'c20acb14a3d3339b9e92daebb173e41379f9f2fad4aa6a6326a696bd90c67419'


    @responses.activate
    @mock.patch('noclist.retry')
    def test_get_users(self, mock_retry):
        """Tests get_users()"""
        responses.add(
            responses.GET,
            url=BASE_URL + '/users',
            status=200
        )

        text = 'aaaaa\nbbbbb\nccccc'
        response = requests.Response()
        response.status_code = 200
        type(response).text = mock.PropertyMock(return_value=text)

        mock_retry.return_value = response
        users = get_users('checksum-12345')
        assert users == text


    def test_get_formatted(self):
        """Tests get_formatted()"""
        text = 'aaaaa\nbbbbb\nccccc'
        jsonified = formatted(text)
        assert jsonified == '["aaaaa", "bbbbb", "ccccc"]'


    @responses.activate
    def test_retry(self):
        """Tests retry()"""
        responses.add(
            responses.GET,
            url=BASE_URL + '/auth',
            status=400
        )

        url = BASE_URL + '/auth'
        response = retry(url)
        self.assertRaises(requests.exceptions.HTTPError, response)
