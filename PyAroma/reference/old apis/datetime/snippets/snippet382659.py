from __future__ import division
from avrogen.logical import DecimalLogicalTypeProcessor, DateLogicalTypeProcessor
from avrogen.logical import TimestampMicrosLogicalTypeProcessor, TimestampMillisLogicalTypeProcessor
from avrogen.logical import TimeMicrosLogicalTypeProcessor, TimeMillisLogicalTypeProcessor
from avro import schema
import unittest
import decimal
import contextlib
import datetime
import pytz
import tzlocal
import time
import six


def test_time_micros(self):
    p = TimeMicrosLogicalTypeProcessor()
    test_schema1 = make_avsc_object('string')
    test_schema2 = make_avsc_object('long')
    test_schema3 = make_avsc_object({'type': 'record', 'name': 'test2', 'fields': [{'name': 'f1', 'type': 'int'}]})
    self.assertFalse(p.can_convert(test_schema1))
    self.assertTrue(p.can_convert(test_schema2))
    self.assertFalse(p.can_convert(test_schema3))
    self.assertFalse(p.does_match(test_schema1, test_schema2))
    self.assertTrue(p.does_match(test_schema2, test_schema2))
    self.assertFalse(p.does_match(test_schema3, test_schema3))
    self.assertEquals(p.convert(test_schema2, datetime.time(23, 24, 25, 123456)), 84265123456)
    with self._exception():
        p.convert('123456')
    self.assertEquals(p.convert_back(test_schema2, test_schema2, 84265123456), datetime.time(23, 24, 25, 123456))
