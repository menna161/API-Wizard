import unittest
from unittest import mock
from unittest.mock import MagicMock
import requests
from requests import HTTPError
from requests import ConnectionError as RequestsConnectionError
from requests import Timeout
import pypco
from pypco.exceptions import PCORequestException
from pypco.exceptions import PCORequestTimeoutException
from pypco.exceptions import PCOUnexpectedRequestException


@mock.patch('requests.post', side_effect=mock_oauth_response)
def test_invalid_code(self, mock_post):
    'Ensure error response with invalid status code'
    with self.assertRaises(PCORequestException) as err_cm:
        pypco.get_oauth_access_token('id', 'secret', 'bad', 'https://www.site.com/')
    self.assertEqual(401, err_cm.exception.status_code)
    self.assertEqual('{"test_key": "test_value"}', err_cm.exception.response_body)
    mock_post.assert_called_once_with('https://api.planningcenteronline.com/oauth/token', data={'client_id': 'id', 'client_secret': 'secret', 'code': 'bad', 'redirect_uri': 'https://www.site.com/', 'grant_type': 'authorization_code'}, headers={'User-Agent': 'pypco'}, timeout=30)
