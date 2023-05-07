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


def day_of_week(start, end, weekday):
    number = utils.weekday_number(weekday)
    floored = utils.datetime_floor(start)
    next_week = (floored + datetime.timedelta(days=7))
    for day in utils.datetime_range(floored, next_week, 'days'):
        if (day.weekday() == number):
            first_day = day
            break
    domain = TimeSeries(default=False)
    for week_start in utils.datetime_range(first_day, end, 'weeks', inclusive_end=True):
        interval_start = week_start
        interval_end = (interval_start + datetime.timedelta(days=1))
        domain[interval_start] = True
        domain[interval_end] = False
    result = domain.slice(start, end)
    result[end] = False
    return result
