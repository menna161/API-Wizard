import math
from datetime import date, datetime
from functools import partial
from leather import utils
from leather.ticks.score import ScoreTicker


def __init__(self, domain_min, domain_max):
    self._domain_min = domain_min
    self._domain_max = domain_max
    if isinstance(self._domain_min, datetime):
        self._type = datetime
    else:
        self._type = date
    self._to_unit = None
    self._from_unit = None
    self._fmt = None
    previous_delta = 0
    for (to_func, from_func, overlap_fmt, simple_fmt) in INTERVALS:
        delta = (to_func(self._domain_max) - to_func(self._domain_min))
        if ((delta >= MIN_UNITS) or (to_func is utils.to_microsecond_count)):
            self._to_unit = to_func
            self._from_unit = partial(from_func, t=self._type)
            if (previous_delta >= 1):
                self._fmt = overlap_fmt
            else:
                self._fmt = simple_fmt
            break
        previous_delta = delta
    self._unit_min = self._to_unit(self._domain_min)
    self._unit_max = self._to_unit(self._domain_max)
    if ((self._domain_max - self._from_unit(self._unit_max)).total_seconds() > 0):
        self._unit_max += 1
    self._ticks = self._find_ticks()
    self._min = self._ticks[0]
    self._max = self._ticks[(- 1)]
