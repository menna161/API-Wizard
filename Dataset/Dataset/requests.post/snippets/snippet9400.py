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


@mock.patch('requests.post', side_effect=Exception)
def test_get_cc_org_token_general_exception(self, mock_get):
    'Ensure error response with invalid status code'
    with self.assertRaises(PCOUnexpectedRequestException):
        pypco.user_auth_helpers.get_cc_org_token('yourcbcfamily')
