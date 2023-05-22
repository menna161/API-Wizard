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
@patch('builtins.open')
def test_do_request(self, mock_fh, mock_request):
    'Test dispatching single requests; HTTP verbs, file uploads, etc.'
    pco = pypco.PCO(application_id='app_id', secret='secret')
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '{"hello": "world"}'
    mock_request.return_value = mock_response
    pco._do_request('GET', 'https://api.planningcenteronline.com/somewhere/v2/something', include='test', per_page=100)
    mock_request.assert_called_with('GET', 'https://api.planningcenteronline.com/somewhere/v2/something', params={'include': 'test', 'per_page': 100}, headers={'User-Agent': 'pypco', 'Authorization': 'Basic YXBwX2lkOnNlY3JldA=='}, json=None, timeout=60)
    pco._do_request('POST', 'https://api.planningcenteronline.com/somewhere/v2/something', payload={'type': 'Person', 'attributes': {'a': 1, 'b': 2}})
    mock_request.assert_called_with('POST', 'https://api.planningcenteronline.com/somewhere/v2/something', json={'type': 'Person', 'attributes': {'a': 1, 'b': 2}}, headers={'User-Agent': 'pypco', 'Authorization': 'Basic YXBwX2lkOnNlY3JldA=='}, params={}, timeout=60)
    mock_fh.name = 'open()'
    pco._do_request('POST', 'https://api.planningcenteronline.com/somewhere/v2/something', upload='/file/path')
    mock_fh.assert_called_once_with('/file/path', 'rb')
