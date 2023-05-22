import csv
import datetime
import itertools
import pprint
from queue import PriorityQueue
import sortedcontainers
from dateutil.parser import parse as date_parse
from infinity import inf
from . import histogram, operations, utils, plot
import pandas as pd


def bin(self, unit, n_units=1, start=None, end=None, mask=None, smaller=None, transform='distribution'):
    if ((mask is not None) and mask.is_empty()):
        return sortedcontainers.SortedDict()
    elif ((start is not None) and (start == end)):
        return sortedcontainers.SortedDict()
    if smaller:
        return self.rebin(smaller, (lambda x: utils.datetime_floor(x, unit, n_units)))
    (start, end, mask) = self._check_boundaries(start, end, mask=mask)
    start = utils.datetime_floor(start, unit=unit, n_units=n_units)
    function = getattr(self, transform)
    result = sortedcontainers.SortedDict()
    dt_range = utils.datetime_range(start, end, unit, n_units=n_units)
    for (bin_start, bin_end) in utils.pairwise(dt_range):
        result[bin_start] = function(bin_start, bin_end, mask=mask, normalized=False)
    return result
