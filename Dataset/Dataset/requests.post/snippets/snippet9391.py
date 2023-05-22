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
def test_http_errors(self, mock_post):
    'Ensure error response with http errors.'
    with self.assertRaises(PCORequestException):
        pypco.user_auth_helpers._do_oauth_post('https://api.planningcenteronline.com/oauth/token', client_id='id', client_secret='secret', code='bad', redirect_uri='https://www.site.com', grant_type='authorization_code')
    with self.assertRaises(PCORequestException):
        pypco.user_auth_helpers._do_oauth_post('https://api.planningcenteronline.com/oauth/token', client_id='id', client_secret='secret', code='server_error', redirect_uri='https://www.site.com', grant_type='authorization_code')
