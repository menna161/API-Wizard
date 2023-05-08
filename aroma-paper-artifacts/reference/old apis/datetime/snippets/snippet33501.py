import datetime
import struct
import time
import sys
import os
from six import string_types, PY3
from ._common import tzname_in_python2
from .win import tzwin, tzwinlocal
from dateutil import relativedelta
from dateutil import parser
from dateutil import rrule
from dateutil.zoneinfo import gettz


def __init__(self, name, offset):
    self._name = name
    self._offset = datetime.timedelta(seconds=offset)
