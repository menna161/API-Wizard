import datetime
from auvsi_suas.models.time_period import TimePeriod
from collections import namedtuple
from django.test import TestCase
from django.utils import timezone


def test_duration_finite(self):
    'Tests the duration with endpoints and finite time.'
    t = TimePeriod(start=datetime.datetime(2000, 1, 1), end=datetime.datetime(2000, 1, 2))
    self.assertEqual(datetime.timedelta(days=1), t.duration())
