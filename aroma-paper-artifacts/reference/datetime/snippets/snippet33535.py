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


def _isdst(self, dt):
    if (not self._start_delta):
        return False
    year = datetime.datetime(dt.year, 1, 1)
    start = (year + self._start_delta)
    end = (year + self._end_delta)
    dt = dt.replace(tzinfo=None)
    if (start < end):
        return ((dt >= start) and (dt < end))
    else:
        return ((dt >= start) or (dt < end))
