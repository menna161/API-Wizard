import unittest
import requests_mock
from saucenao.http import *


@requests_mock.mock()
def test_status_code_api_key(self, mock):
    'Test the verify status code function for 403 wrong api key status\n\n        :return:\n        '
    mock.get(self.dummy_url, text='', status_code=403)
    with self.assertRaises(InvalidOrWrongApiKeyException) as _:
        verify_status_code(request_response=requests.get(self.dummy_url))
