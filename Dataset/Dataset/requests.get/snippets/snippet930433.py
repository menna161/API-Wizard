from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unittest
import mock
import requests
from official.utils.logs import cloud_lib


@mock.patch('requests.get')
def test_on_gcp(self, mock_requests_get):
    mock_response = mock.MagicMock()
    mock_requests_get.return_value = mock_response
    mock_response.status_code = 200
    self.assertEqual(cloud_lib.on_gcp(), True)
