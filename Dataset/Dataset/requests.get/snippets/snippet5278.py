import unittest
import requests_mock
from saucenao.http import *


@requests_mock.mock()
def test_status_code_ok(self, mock):
    'Test the verify status code function for 200 ok status code\n\n        :return:\n        '
    mock.get(self.dummy_url, status_code=200)
    (status_code, msg) = verify_status_code(request_response=requests.get(self.dummy_url))
    self.assertEqual(status_code, STATUS_CODE_OK)
