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


def test_timestamp_millis(self):
    p = TimestampMillisLogicalTypeProcessor()
    test_schema1 = make_avsc_object('string')
    test_schema2 = make_avsc_object('long')
    test_schema3 = make_avsc_object({'type': 'record', 'name': 'test2', 'fields': [{'name': 'f1', 'type': 'int'}]})
    self.assertFalse(p.can_convert(test_schema1))
    self.assertTrue(p.can_convert(test_schema2))
    self.assertFalse(p.can_convert(test_schema3))
    self.assertFalse(p.does_match(test_schema1, test_schema2))
    self.assertTrue(p.does_match(test_schema2, test_schema2))
    self.assertFalse(p.does_match(test_schema3, test_schema3))
    dt1 = datetime.datetime(2015, 5, 1)
    self.assertEquals(p.convert(test_schema2, datetime.date(2015, 5, 1)), p.convert(test_schema2, dt1))
    self.assertEquals(p.convert(test_schema2, datetime.datetime(2015, 5, 1, microsecond=123456, tzinfo=pytz.UTC)), 1430438400123)
    offset_res = 1430452800123
    self.assertEquals(p.convert(test_schema2, pytz.timezone('America/New_York').localize(datetime.datetime(2015, 5, 1, microsecond=123456))), offset_res)
    with self._exception():
        p.convert('123456')
    self.assertEquals(p.convert_back(test_schema2, test_schema2, p.convert(test_schema2, datetime.datetime(2016, 1, 1))), datetime.datetime(2016, 1, 1))
