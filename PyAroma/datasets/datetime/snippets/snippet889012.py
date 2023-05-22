import warnings
from collections import namedtuple
from datetime import date, datetime, timedelta
from decimal import Decimal
from IPython.display import SVG as IPythonSVG


def to_hour_count(d):
    '\n    date > n hours\n    '
    return ((d - datetime.min).total_seconds() / (60 * 60))
