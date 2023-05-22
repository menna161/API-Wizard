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


@mock.patch('requests.post')
def test_get_cc_org_token_raise_for_status(self, mock_requests):
    'Ensure error response with invalid status code'
    exception = HTTPError(mock.Mock(status=404), 'not found')
    mock_requests(mock.ANY).raise_for_status.side_effect = exception
    with self.assertRaises(PCORequestException):
        pypco.user_auth_helpers.get_cc_org_token('yourcbcfamily')
