import itertools
import datetime
import calendar
import sys
from six import advance_iterator, integer_types
from six.moves import _thread
import heapq
from warnings import warn
from math import gcd
from fractions import gcd
from dateutil import parser
from dateutil import easter
from dateutil import parser
from dateutil import parser


def after(self, dt, inc=False):
    ' Returns the first recurrence after the given datetime instance. The\n            inc keyword defines what happens if dt is an occurrence. With\n            inc=True, if dt itself is an occurrence, it will be returned.  '
    if self._cache_complete:
        gen = self._cache
    else:
        gen = self
    if inc:
        for i in gen:
            if (i >= dt):
                return i
    else:
        for i in gen:
            if (i > dt):
                return i
    return None
