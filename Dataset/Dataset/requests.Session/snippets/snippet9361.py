import os
import json
from unittest.mock import Mock, patch
import requests
from requests.exceptions import SSLError
import pypco
from pypco.exceptions import PCORequestTimeoutException, PCORequestException, PCOUnexpectedRequestException
from pypco.auth_config import PCOAuthConfig
from tests import BasePCOTestCase, BasePCOVCRTestCase


@patch('requests.Session.request', side_effect=ratelimit_se)
@patch('time.sleep')
def test_do_ratelimit_managed_request(self, mock_sleep, mock_request):
    'Test automatic rate limit handling.'
    global RL_REQUEST_COUNT, RL_LIMITED_REQUESTS
    pco = pypco.PCO('app_id', 'secret')
    RL_REQUEST_COUNT = 0
    RL_LIMITED_REQUESTS = 0
    pco._do_ratelimit_managed_request('GET', '/test')
    mock_request.assert_called_once()
    mock_sleep.assert_not_called()
    RL_REQUEST_COUNT = 1
    RL_LIMITED_REQUESTS = 0
    pco._do_ratelimit_managed_request('GET', '/test')
    mock_sleep.assert_called_once_with(5)
    RL_REQUEST_COUNT = 3
    RL_LIMITED_REQUESTS = 0
    result = pco._do_ratelimit_managed_request('GET', '/test')
    mock_sleep.assert_called_with(15)
    self.assertIsNotNone(result, "Didn't get response returned!")
