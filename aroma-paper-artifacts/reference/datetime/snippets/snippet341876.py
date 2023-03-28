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


@writable_property
def release_date(self):
    'The date on which the release was published (a :class:`~datetime.date` object).'
