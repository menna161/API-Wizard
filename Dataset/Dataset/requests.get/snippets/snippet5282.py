import unittest
import requests_mock
from saucenao.http import *


@requests_mock.mock()
def test_status_code_limit(self, mock):
    'Test the verify status code function for 429 limit reached status\n\n        :return:\n        '
    mock.get(self.dummy_url, text='limit of 150 searches reached', status_code=429)
    with self.assertRaises(DailyLimitReachedException) as exception:
        verify_status_code(request_response=requests.get(self.dummy_url))
        self.assertEqual(str(exception), 'Daily search limit for unregistered users reached')
    mock.get(self.dummy_url, text='limit of 300 searches reached', status_code=429)
    with self.assertRaises(DailyLimitReachedException) as exception:
        verify_status_code(request_response=requests.get(self.dummy_url))
        self.assertEqual(str(exception), 'Daily search limit for basic users reached')
    mock.get(self.dummy_url, status_code=429)
    with self.assertRaises(DailyLimitReachedException) as exception:
        verify_status_code(request_response=requests.get(self.dummy_url))
        self.assertEqual(str(exception), 'Daily search limit reached')
