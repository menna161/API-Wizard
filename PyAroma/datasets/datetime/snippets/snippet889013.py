import warnings
from collections import namedtuple
from datetime import date, datetime, timedelta
from decimal import Decimal
from IPython.display import SVG as IPythonSVG


def from_hour_count(n, t=datetime):
    '\n    n hours > date\n    '
    return (t.min + timedelta(hours=n))
