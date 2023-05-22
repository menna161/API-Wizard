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


def moving_average(self, sampling_period, window_size=None, start=None, end=None, placement='center', pandas=False):
    'Averaging over regular intervals\n        '
    (start, end, mask) = self._check_boundaries(start, end)
    if (window_size is None):
        window_size = sampling_period
    sampling_period = self._check_regularization(start, end, sampling_period)
    full_window = (window_size * 1.0)
    half_window = (full_window / 2)
    if (isinstance(start, datetime.date) and (not isinstance(full_window, datetime.timedelta))):
        half_window = datetime.timedelta(seconds=half_window)
        full_window = datetime.timedelta(seconds=full_window)
    result = []
    current_time = start
    while (current_time <= end):
        if (placement == 'center'):
            window_start = (current_time - half_window)
            window_end = (current_time + half_window)
        elif (placement == 'left'):
            window_start = current_time
            window_end = (current_time + full_window)
        elif (placement == 'right'):
            window_start = (current_time - full_window)
            window_end = current_time
        else:
            msg = 'unknown placement "{}"'.format(placement)
            raise ValueError(msg)
        try:
            mean = self.mean(window_start, window_end)
        except TypeError as e:
            if ('NoneType' in str(e)):
                mean = None
            else:
                raise e
        result.append((current_time, mean))
        current_time += sampling_period
    if pandas:
        try:
            import pandas as pd
        except ImportError:
            msg = "can't have pandas=True if pandas is not installed"
            raise ImportError(msg)
        result = pd.Series([v for (t, v) in result], index=[t for (t, v) in result])
    return result
