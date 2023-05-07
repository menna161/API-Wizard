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


def distribution(self, start=None, end=None, normalized=True, mask=None, interpolate='previous'):
    'Calculate the distribution of values over the given time range from\n        `start` to `end`.\n\n        Args:\n\n            start (orderable, optional): The lower time bound of\n                when to calculate the distribution. By default, the\n                first time point will be used.\n\n            end (orderable, optional): The upper time bound of\n                when to calculate the distribution. By default, the\n                last time point will be used.\n\n            normalized (bool): If True, distribution will sum to\n                one. If False and the time values of the TimeSeries\n                are datetimes, the units will be seconds.\n\n            mask (:obj:`TimeSeries`, optional): A domain on which to\n                calculate the distribution.\n\n            interpolate (str, optional): Method for interpolating\n                between measurement points: either "previous"\n                (default) or "linear". Note: if "previous" is used,\n                then the resulting histogram is exact. If "linear" is\n                given, then the values used for the histogram are the\n                average value for each segment -- the mean of this\n                histogram will be exact, but higher moments (variance)\n                will be approximate.\n\n        Returns:\n\n            :obj:`Histogram` with the results.\n\n        '
    (start, end, mask) = self._check_boundaries(start, end, mask=mask)
    counter = histogram.Histogram()
    for (i_start, i_end, _) in mask.iterperiods(value=True):
        for (t0, t1, _) in self.iterperiods(i_start, i_end):
            duration = utils.duration_to_number((t1 - t0), units='seconds')
            midpoint = utils.time_midpoint(t0, t1)
            value = self.get(midpoint, interpolate=interpolate)
            try:
                counter[value] += duration
            except histogram.UnorderableElements:
                counter = histogram.Histogram.from_dict(dict(counter), key=hash)
                counter[value] += duration
    if normalized:
        return counter.normalized()
    else:
        return counter
