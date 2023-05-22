import datetime
import sys
from collections import OrderedDict


def str_to_datetime(dtstr, strftime='%Y-%m-%dT%H:%M:%SZ'):
    if (not isinstance(dtstr, basestring)):
        raise TypeError("It's not a string.")
    return datetime.datetime.strptime(dtstr, strftime)
