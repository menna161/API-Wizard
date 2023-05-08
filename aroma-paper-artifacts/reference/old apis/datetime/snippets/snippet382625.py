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


def typename(self):
    return 'datetime.date'
