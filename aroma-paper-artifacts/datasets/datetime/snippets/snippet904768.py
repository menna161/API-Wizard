from __future__ import print_function
import datetime
import sys
import time
from loghub.external.github import ApiError, ApiNotFoundError, GitHub


@staticmethod
def str_to_date(string):
    'Convert ISO date string to datetime object.'
    parts = string.split('T')
    date_parts = parts[0]
    time_parts = parts[1][:(- 1)]
    (year, month, day) = [int(i) for i in date_parts.split('-')]
    (hour, minutes, seconds) = [int(i) for i in time_parts.split(':')]
    return datetime.datetime(year, month, day, hour, minutes, seconds)
