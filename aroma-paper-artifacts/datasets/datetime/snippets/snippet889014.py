import warnings
from collections import namedtuple
from datetime import date, datetime, timedelta
from decimal import Decimal
from IPython.display import SVG as IPythonSVG


def to_minute_count(d):
    '\n    date > n minutes\n    '
    return ((d - datetime.min).total_seconds() / 60)
