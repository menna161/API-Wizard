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
    if (not isinstance(value, datetime.date)):
        raise Exception('Wrong type for date conversion')
    return ((value - EPOCH_DATE).total_seconds() // SECONDS_IN_DAY)
