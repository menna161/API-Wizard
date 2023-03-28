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


def __init__(self, stdabbr, stdoffset=None, dstabbr=None, dstoffset=None, start=None, end=None):
    global relativedelta
    if (not relativedelta):
        from dateutil import relativedelta
    self._std_abbr = stdabbr
    self._dst_abbr = dstabbr
    if (stdoffset is not None):
        self._std_offset = datetime.timedelta(seconds=stdoffset)
    else:
        self._std_offset = ZERO
    if (dstoffset is not None):
        self._dst_offset = datetime.timedelta(seconds=dstoffset)
    elif (dstabbr and (stdoffset is not None)):
        self._dst_offset = (self._std_offset + datetime.timedelta(hours=(+ 1)))
    else:
        self._dst_offset = ZERO
    if (dstabbr and (start is None)):
        self._start_delta = relativedelta.relativedelta(hours=(+ 2), month=4, day=1, weekday=relativedelta.SU((+ 1)))
    else:
        self._start_delta = start
    if (dstabbr and (end is None)):
        self._end_delta = relativedelta.relativedelta(hours=(+ 1), month=10, day=31, weekday=relativedelta.SU((- 1)))
    else:
        self._end_delta = end
