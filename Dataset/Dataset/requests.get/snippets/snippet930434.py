from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import unittest
import mock
import requests
from official.utils.logs import cloud_lib


@mock.patch('requests.get')
def test_not_on_gcp(self, mock_requests_get):
    mock_requests_get.side_effect = requests.exceptions.ConnectionError()
    self.assertEqual(cloud_lib.on_gcp(), False)
