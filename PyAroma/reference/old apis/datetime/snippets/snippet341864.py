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


def parse_date_wiki(value):
    'Convert a string such as ``19 December 2018`` ``August 02, 2019\\n`` to a :class:`datetime.date` object.'
    value = parse_data_wiki(value)
    if (value == 'Unknown'):
        value = '30 April 2008'
    if (len(value) < 15):
        if (not value[:1].isdigit()):
            value = ('30 ' + value)
        if (len(value) < 5):
            value = ('30 April ' + value)
    try:
        return (datetime.datetime.strptime(value, '%d %B %Y').date() if value else None)
    except ValueError:
        return (datetime.datetime.strptime(value, '%B %d, %Y').date() if value else None)
