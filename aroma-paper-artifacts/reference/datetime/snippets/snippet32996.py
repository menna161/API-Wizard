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
def exdate(self, exdate):
    ' Include the given datetime instance in the recurrence set\n            exclusion list. Dates included that way will not be generated,\n            even if some inclusive rrule or rdate matches them. '
    self._exdate.append(exdate)
