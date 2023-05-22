import datetime
import sys
from collections import OrderedDict


def _key_equal_value(k, v):
    if isinstance(v, datetime.datetime):
        v = datetime_to_str(v)
    elif isinstance(v, bool):
        v = str(v).lower()
    elif (not isinstance(v, basestring)):
        v = str(v)
    else:
        v = (('"' + str(v)) + '"')
    return (((k + ' = ') + _utf_8(v)) + '\n')
