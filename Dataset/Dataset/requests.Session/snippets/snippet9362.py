import os
import json
from unittest.mock import Mock, patch
import requests
from requests.exceptions import SSLError
import pypco
from pypco.exceptions import PCORequestTimeoutException, PCORequestException, PCOUnexpectedRequestException
from pypco.auth_config import PCOAuthConfig
from tests import BasePCOTestCase, BasePCOVCRTestCase


@patch('requests.Session.request')
def test_do_url_managed_request(self, mock_request):
    'Test requests with URL cleanup.'
    base = 'https://api.planningcenteronline.com'
    pco = pypco.PCO('app_id', 'secret')
    pco._do_url_managed_request('GET', '/test')
    mock_request.assert_called_with('GET', f'{base}/test', headers={'User-Agent': 'pypco', 'Authorization': 'Basic YXBwX2lkOnNlY3JldA=='}, json=None, params={}, timeout=60)
    pco._do_url_managed_request('GET', 'https://api.planningcenteronline.com/test')
    mock_request.assert_called_with('GET', f'{base}/test', headers={'User-Agent': 'pypco', 'Authorization': 'Basic YXBwX2lkOnNlY3JldA=='}, json=None, params={}, timeout=60)
    pco._do_url_managed_request('GET', 'https://api.planningcenteronline.com//test')
    mock_request.assert_called_with('GET', f'{base}/test', headers={'User-Agent': 'pypco', 'Authorization': 'Basic YXBwX2lkOnNlY3JldA=='}, json=None, params={}, timeout=60)
    pco._do_url_managed_request('GET', 'https://api.planningcenteronline.com//test')
    mock_request.assert_called_with('GET', f'{base}/test', headers={'User-Agent': 'pypco', 'Authorization': 'Basic YXBwX2lkOnNlY3JldA=='}, json=None, params={}, timeout=60)
    pco._do_url_managed_request('GET', 'https://api.planningcenteronline.com//test///test1/test2/////test3/test4')
    mock_request.assert_called_with('GET', f'{base}/test/test1/test2/test3/test4', headers={'User-Agent': 'pypco', 'Authorization': 'Basic YXBwX2lkOnNlY3JldA=='}, json=None, params={}, timeout=60)
