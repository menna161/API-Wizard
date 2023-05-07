import datetime
from auvsi_suas.models.time_period import TimePeriod
from collections import namedtuple
from django.test import TestCase
from django.utils import timezone


def test_within_standard(self):
    'Tests the within method with defined start and end.'
    t = TimePeriod(start=datetime.datetime(2000, 1, 1), end=datetime.datetime(2001, 1, 1))
    self.assertTrue(t.within(datetime.datetime(2000, 6, 1)))
    self.assertTrue(t.within(datetime.datetime(2000, 1, 1)))
    self.assertTrue(t.within(datetime.datetime(2001, 1, 1)))
    self.assertFalse(t.within(datetime.datetime(1999, 1, 1)))
    self.assertFalse(t.within(datetime.datetime(2002, 1, 1)))
