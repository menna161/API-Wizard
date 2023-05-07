import warnings
from collections import namedtuple
from datetime import date, datetime, timedelta
from decimal import Decimal
from IPython.display import SVG as IPythonSVG


def to_microsecond_count(d):
    '\n    date > n microseconds\n    '
    return ((d - datetime.min).total_seconds() * 1000)
