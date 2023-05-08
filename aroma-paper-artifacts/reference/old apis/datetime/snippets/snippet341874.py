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


@lazy_property
def is_eol(self):
    'Whether the release has reached its end-of-life date (a boolean or :data:`None`).'
    eol_date = (self.extended_eol_date or self.eol_date)
    if eol_date:
        return (datetime.date.today() >= eol_date)
    else:
        return False
