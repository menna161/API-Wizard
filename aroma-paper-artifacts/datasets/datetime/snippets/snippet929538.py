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


def hour_of_day(start, end, hour):
    floored = utils.datetime_floor(start)
    domain = TimeSeries(default=False)
    for day_start in utils.datetime_range(floored, end, 'days', inclusive_end=True):
        interval_start = (day_start + datetime.timedelta(hours=hour))
        interval_end = (interval_start + datetime.timedelta(hours=1))
        domain[interval_start] = True
        domain[interval_end] = False
    result = domain.slice(start, end)
    result[end] = False
    return result
