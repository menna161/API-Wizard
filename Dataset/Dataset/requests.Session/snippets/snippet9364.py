import os
import json
from unittest.mock import Mock, patch
import requests
from requests.exceptions import SSLError
import pypco
from pypco.exceptions import PCORequestTimeoutException, PCORequestException, PCOUnexpectedRequestException
from pypco.auth_config import PCOAuthConfig
from tests import BasePCOTestCase, BasePCOVCRTestCase


@patch('requests.Session.request', side_effect=connection_error_se)
def test_request_resonse_general_err(self, _):
    'Test the request_response() function when a general error is thrown.'
    pco = self.pco
    with self.assertRaises(PCOUnexpectedRequestException):
        pco.request_response('GET', '/test')
