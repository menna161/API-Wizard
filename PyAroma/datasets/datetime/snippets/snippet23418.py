import datetime
import sys
from collections import OrderedDict


def datetime_to_str(dttime, strftime='%Y-%m-%dT%H:%M:%SZ'):
    if (not isinstance(dttime, datetime.datetime)):
        raise TypeError("It's not a datetime.")
    return dttime.strftime(strftime)
