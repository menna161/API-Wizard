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
    value = (long(value) / 1000000.0)
    utc = datetime.datetime.utcfromtimestamp(value).replace(tzinfo=pytz.UTC)
    return utc.astimezone(tzlocal.get_localzone()).replace(tzinfo=None)
