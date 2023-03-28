import datetime
import os
import string
import unittest
from google.appengine.ext import ndb
from google.appengine.api import namespace_manager
from google.appengine.ext import db
from google.appengine.ext import testbed
from mapreduce import property_range


def testSplitDateTimeProperty(self):
    start = datetime.datetime(1, 1, 1, 0, 0, 0, 0)
    end = datetime.datetime(1, 1, 1, 0, 0, 0, 3)
    self.assertEquals([start, datetime.datetime(1, 1, 1, 0, 0, 0, 1), datetime.datetime(1, 1, 1, 0, 0, 0, 2), end, datetime.datetime(1, 1, 1, 0, 0, 0, 4)], property_range._split_datetime_property(start, end, 4, True, True))
    self.assertEquals([start, datetime.datetime(1, 1, 1, 0, 0, 0, 1), datetime.datetime(1, 1, 1, 0, 0, 0, 2), end], property_range._split_datetime_property(start, end, 3, True, False))
    self.assertEquals([datetime.datetime(1, 1, 1, 0, 0, 0, 1), datetime.datetime(1, 1, 1, 0, 0, 0, 2), end, datetime.datetime(1, 1, 1, 0, 0, 0, 4)], property_range._split_datetime_property(start, end, 3, False, True))
    end = datetime.datetime(1, 1, 1, 0, 0, 0, 100)
    self.assertEquals([datetime.datetime(1, 1, 1, 0, 0, 0, 1), datetime.datetime(1, 1, 1, 0, 0, 0, 34), datetime.datetime(1, 1, 1, 0, 0, 0, 67), datetime.datetime(1, 1, 1, 0, 0, 0, 101)], property_range._split_datetime_property(start, end, 3, False, True))
    end = datetime.datetime(1, 1, 1, 0, 0, 0, 1)
    self.assertRaises(ValueError, property_range._split_datetime_property, start, end, 10, False, False)
