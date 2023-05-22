import datetime
import os
import string
import unittest
from google.appengine.ext import ndb
from google.appengine.api import namespace_manager
from google.appengine.ext import db
from google.appengine.ext import testbed
from mapreduce import property_range


def testGetRangeFromFilters(self):
    'Tests validating filters parameter.'
    new = datetime.datetime.now()
    old = new.replace(year=(new.year - 1))
    filters = [('a', '=', 1), ('b', '=', 2)]
    (prop, start, end) = property_range.PropertyRange._get_range_from_filters(filters, TestEntity)
    self.assertEquals(prop, None)
    self.assertEquals(start, None)
    self.assertEquals(end, None)
    filters = [['a', '>', 1], ['a', '<', 2]]
    (prop, start, end) = property_range.PropertyRange._get_range_from_filters(filters, TestEntity)
    self.assertEquals(prop, TestEntity.a)
    self.assertEquals(start, ['a', '>', 1])
    self.assertEquals(end, ['a', '<', 2])
    filters = [['datetime_property', '>', old], ['datetime_property', '<=', new], ['a', '=', 1]]
    (prop, start, end) = property_range.PropertyRange._get_range_from_filters(filters, TestEntity)
    self.assertEquals(prop, TestEntity.datetime_property)
    self.assertEquals(start, ['datetime_property', '>', old])
    self.assertEquals(end, ['datetime_property', '<=', new])
    filters = [('a', '<=', 1)]
    self.assertRaises(property_range.errors.BadReaderParamsError, property_range.PropertyRange._get_range_from_filters, filters, TestEntity)
    filters = [['datetime_property', '>', new], ['datetime_property', '<=', old]]
    self.assertRaises(property_range.errors.BadReaderParamsError, property_range.PropertyRange._get_range_from_filters, filters, TestEntity)
