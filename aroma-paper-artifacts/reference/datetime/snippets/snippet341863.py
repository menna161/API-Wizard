import csv
import datetime
import decimal
import glob
import logging
import numbers
import os
import six
from executor import execute
from humanfriendly.decorators import cached
from six import string_types
from itertools import product
from property_manager3 import PropertyManager, key_property, lazy_property, required_property, writable_property
from apt_smart.backends.debian import LTS_RELEASES
from property_manager import PropertyManager, key_property, lazy_property, required_property, writable_property


def parse_date(value):
    'Convert a ``YYYY-MM-DD`` string to a :class:`datetime.date` object.'
    return (datetime.datetime.strptime(value, '%Y-%m-%d').date() if value else None)
