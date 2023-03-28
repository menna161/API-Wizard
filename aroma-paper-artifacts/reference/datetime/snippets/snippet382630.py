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


def convert_back(self, writers_schema, readers_schema, value):
    (_, hours, minutes, seconds, microseconds) = TimeMicrosLogicalTypeProcessor.extract_time_parts(value)
    return datetime.time(hours, minutes, seconds, microseconds)
