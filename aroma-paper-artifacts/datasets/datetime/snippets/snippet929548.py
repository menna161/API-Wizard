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


def _get_linear_interpolate(self, time):
    right_index = self._d.bisect_right(time)
    left_index = (right_index - 1)
    if (left_index < 0):
        return self.default
    elif (right_index == len(self._d)):
        return self.last_item()[1]
    else:
        (left_time, left_value) = self._d.peekitem(left_index)
        (right_time, right_value) = self._d.peekitem(right_index)
        dt_interval = (right_time - left_time)
        dt_start = (time - left_time)
        if isinstance(dt_interval, datetime.timedelta):
            dt_interval = dt_interval.total_seconds()
            dt_start = dt_start.total_seconds()
        slope = (float((right_value - left_value)) / dt_interval)
        value = ((slope * dt_start) + left_value)
        return value
