import datetime
import io
import unittest
from unittest import mock
from aranet4 import client
from aranet4 import aranetctl


def test_log_times_1(self):
    log_records = 13
    log_interval = 300
    expected = []
    expected_start = datetime.datetime(2000, 10, 11, 22, 59, 10)
    for idx in range(log_records):
        expected.append((expected_start + datetime.timedelta(seconds=(log_interval * idx))))
    now = datetime.datetime(2000, 10, 11, 23, 59, 30)
    times = client._log_times(now, log_records, log_interval, 20)
    self.assertListEqual(expected, times)
