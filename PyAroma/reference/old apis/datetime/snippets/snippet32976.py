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


def xafter(self, dt, count=None, inc=False):
    '\n        Generator which yields up to `count` recurrences after the given\n        datetime instance, equivalent to `after`.\n\n        :param dt:\n            The datetime at which to start generating recurrences.\n\n        :param count:\n            The maximum number of recurrences to generate. If `None` (default),\n            dates are generated until the recurrence rule is exhausted.\n\n        :param inc:\n            If `dt` is an instance of the rule and `inc` is `True`, it is\n            included in the output.\n\n        :yields: Yields a sequence of `datetime` objects.\n        '
    if self._cache_complete:
        gen = self._cache
    else:
        gen = self
    if inc:
        comp = (lambda dc, dtc: (dc >= dtc))
    else:
        comp = (lambda dc, dtc: (dc > dtc))
    n = 0
    for d in gen:
        if comp(d, dt):
            (yield d)
            if (count is not None):
                n += 1
                if (n >= count):
                    break
