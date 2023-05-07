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


def _check_regularization(self, start, end, sampling_period=None):
    if (sampling_period is not None):
        if isinstance(sampling_period, datetime.timedelta):
            sampling_period_seconds = sampling_period.total_seconds()
            sampling_period_timedelta = sampling_period
        else:
            sampling_period_seconds = sampling_period
            sampling_period_timedelta = datetime.timedelta(seconds=sampling_period)
        if (sampling_period_seconds <= 0):
            msg = 'sampling_period must be > 0'
            raise ValueError(msg)
        if (sampling_period_seconds > utils.duration_to_number((end - start))):
            msg = 'sampling_period is greater than the duration between start and end.'
            raise ValueError(msg)
        if isinstance(start, datetime.date):
            sampling_period = sampling_period_timedelta
        else:
            sampling_period = sampling_period_seconds
    return sampling_period
