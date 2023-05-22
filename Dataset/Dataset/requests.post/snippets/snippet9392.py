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
def test_successful_post(self, mock_post):
    'Ensure successful post request execution with correct parameters.'
    response = pypco.user_auth_helpers._do_oauth_post('https://api.planningcenteronline.com/oauth/token', client_id='id', client_secret='secret', code='good', redirect_uri='https://www.site.com', grant_type='authorization_code')
    self.assertEqual(200, response.status_code)
    mock_post.assert_called_once_with('https://api.planningcenteronline.com/oauth/token', data={'client_id': 'id', 'client_secret': 'secret', 'code': 'good', 'redirect_uri': 'https://www.site.com', 'grant_type': 'authorization_code'}, headers={'User-Agent': 'pypco'}, timeout=30)
