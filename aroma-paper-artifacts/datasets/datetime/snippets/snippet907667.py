import bisect
import collections
import datetime
import warnings
from dateutil.parser import parse as _dateutil_parse


def _simpleparsefun(date):
    'Simple date parsing function'
    if hasattr(date, 'year'):
        return date
    try:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return date
