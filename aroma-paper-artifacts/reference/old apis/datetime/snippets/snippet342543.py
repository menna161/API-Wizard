import datetime
import io
import unittest
from unittest import mock
from aranet4 import client
from aranet4 import aranetctl


def test_calc_log_last_n(self):
    mock_points = ([datetime.datetime.now(datetime.timezone.utc)] * 200)
    (start, end) = client._calc_start_end(mock_points, {'last': 20})
    self.assertEqual(181, start)
    self.assertEqual(200, end)
    self.assertEqual(19, (end - start))
