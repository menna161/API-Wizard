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
    if (not isinstance(value, datetime.time)):
        raise Exception('Wrong type for time conversion')
    return ((((((value.hour * 60) + value.minute) * 60) + value.second) * 1000000) + value.microsecond)
