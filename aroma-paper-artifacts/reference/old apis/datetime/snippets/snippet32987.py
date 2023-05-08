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


def wdayset(self, year, month, day):
    dset = ([None] * (self.yearlen + 7))
    i = (datetime.date(year, month, day).toordinal() - self.yearordinal)
    start = i
    for j in range(7):
        dset[i] = i
        i += 1
        if (self.wdaymask[i] == self.rrule._wkst):
            break
    return (dset, start, i)
