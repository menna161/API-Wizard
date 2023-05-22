import os
import json
from unittest.mock import Mock, patch
import requests
from requests.exceptions import SSLError
import pypco
from pypco.exceptions import PCORequestTimeoutException, PCORequestException, PCOUnexpectedRequestException
from pypco.auth_config import PCOAuthConfig
from tests import BasePCOTestCase, BasePCOVCRTestCase


@patch('requests.Session.request', side_effect=timeout_se)
def test_do_timeout_managed_request(self, mock_request):
    'Test requests that automatically will retry on timeout.'
    global REQUEST_COUNT, TIMEOUTS
    pco = pypco.PCO(application_id='app_id', secret='secret')
    REQUEST_COUNT = 0
    TIMEOUTS = 0
    pco._do_timeout_managed_request('GET', '/test')
    self.assertEqual(REQUEST_COUNT, 1, 'Successful request not executed exactly once.')
    REQUEST_COUNT = 0
    TIMEOUTS = 1
    pco._do_timeout_managed_request('GET', '/test')
    self.assertEqual(REQUEST_COUNT, 2, 'Successful request not executed exactly once.')
    REQUEST_COUNT = 0
    TIMEOUTS = 1
    pco._do_timeout_managed_request('GET', '/test')
    self.assertEqual(REQUEST_COUNT, 2, 'Successful request not executed exactly once.')
    REQUEST_COUNT = 0
    TIMEOUTS = 2
    pco._do_timeout_managed_request('GET', '/test')
    self.assertEqual(REQUEST_COUNT, 3, 'Successful request not executed exactly once.')
    REQUEST_COUNT = 0
    TIMEOUTS = 3
    with self.assertRaises(PCORequestTimeoutException):
        pco._do_timeout_managed_request('GET', '/test')
    mock_request.assert_called_with('GET', '/test', headers={'User-Agent': 'pypco', 'Authorization': 'Basic YXBwX2lkOnNlY3JldA=='}, json=None, params={}, timeout=60)
    pco = pypco.PCO(application_id='app_id', secret='secret', timeout_retries=2)
    REQUEST_COUNT = 0
    TIMEOUTS = 2
    with self.assertRaises(PCORequestTimeoutException):
        pco._do_timeout_managed_request('GET', '/test')
