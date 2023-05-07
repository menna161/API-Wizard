import datetime
from auvsi_suas.models.time_period import TimePeriod
from collections import namedtuple
from django.test import TestCase
from django.utils import timezone


def test_within_no_start(self):
    'Tests the within method with defined end and no start.'
    t = TimePeriod(end=datetime.datetime(2001, 1, 1))
    self.assertTrue(t.within(datetime.datetime(2000, 6, 1)))
    self.assertTrue(t.within(datetime.datetime(2001, 1, 1)))
    self.assertTrue(t.within(datetime.datetime(1999, 1, 1)))
    self.assertFalse(t.within(datetime.datetime(2002, 1, 1)))
