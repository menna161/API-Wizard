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


@_invalidates_cache
def rdate(self, rdate):
    ' Include the given :py:class:`datetime` instance in the recurrence\n            set generation. '
    self._rdate.append(rdate)
