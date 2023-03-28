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


def initializer(self, value=None):
    return (('logical.TimestampMillisLogicalTypeProcessor().convert_back(None, None, %s)' % value) if (value is not None) else 'datetime.datetime.now()')
