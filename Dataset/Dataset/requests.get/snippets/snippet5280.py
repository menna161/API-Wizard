import unittest
import requests_mock
from saucenao.http import *


@requests_mock.mock()
def test_status_code_repeat(self, mock):
    'Test the verify status code function with multiple mock request responses\n\n        :return:\n        '
    mock.get(self.dummy_url, text='', status_code=999)
    (status_code, msg) = verify_status_code(request_response=requests.get(self.dummy_url))
    self.assertEqual(status_code, STATUS_CODE_REPEAT)
