from __future__ import division
from avro import schema, io
import functools
import abc
import six
import collections
import frozendict
import datetime
import decimal
import struct
import time
import pytz
import tzlocal


def convert(self, writers_schema, value):
    if (not isinstance(value, datetime.datetime)):
        if isinstance(value, datetime.date):
            value = tzlocal.get_localzone().localize(datetime.datetime(value.year, value.month, value.day, 0, 0, 0, 0))
    if (value.tzinfo is None):
        value = tzlocal.get_localzone().localize(value)
    value = ((time.mktime(value.utctimetuple()) - EPOCH_TT) + (value.microsecond / 1000000.0))
    return long((value * 1000000))
