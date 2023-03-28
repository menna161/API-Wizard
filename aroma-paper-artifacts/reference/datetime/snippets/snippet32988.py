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


def ddayset(self, year, month, day):
    dset = ([None] * self.yearlen)
    i = (datetime.date(year, month, day).toordinal() - self.yearordinal)
    dset[i] = i
    return (dset, i, (i + 1))
