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


def stimeset(self, hour, minute, second):
    return (datetime.time(hour, minute, second, tzinfo=self.rrule._tzinfo),)
