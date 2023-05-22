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
def test_valid_refresh_token(self, mock_post):
    'Verify successful refresh with valid token.'
    self.assertIn('access_token', list(pypco.get_oauth_refresh_token('id', 'secret', 'refresh_good').keys()))
    mock_post.assert_called_once_with('https://api.planningcenteronline.com/oauth/token', data={'client_id': 'id', 'client_secret': 'secret', 'refresh_token': 'refresh_good', 'grant_type': 'refresh_token'}, headers={'User-Agent': 'pypco'}, timeout=30)
