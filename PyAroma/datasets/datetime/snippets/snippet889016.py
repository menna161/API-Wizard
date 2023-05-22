import warnings
from collections import namedtuple
from datetime import date, datetime, timedelta
from decimal import Decimal
from IPython.display import SVG as IPythonSVG


def to_second_count(d):
    '\n    date > n seconds\n    '
    return (d - datetime.min).total_seconds()
