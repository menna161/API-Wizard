import datetime
from auvsi_suas.models.time_period import TimePeriod
from collections import namedtuple
from django.test import TestCase
from django.utils import timezone


def test_duration_infinite(self):
    'Tests the duration with infinite value (no endpoint).'
    t = TimePeriod(start=datetime.datetime(2000, 1, 1))
    self.assertIsNone(t.duration())
    t = TimePeriod(end=datetime.datetime(2000, 1, 1))
    self.assertIsNone(t.duration())
