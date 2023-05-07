import datetime
import sys
from collections import OrderedDict


def _str_transition_obj(v):
    if (not isinstance(v, basestring)):
        raise TypeError("It's not a string")
    if (v.lower() == 'true'):
        return True
    elif (v.lower() == 'false'):
        return False
    try:
        if _re('\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z', v):
            return str_to_datetime(v)
    except Exception as e:
        raise e
    try:
        _veal = eval(v.replace(',', ', '))
        if isinstance(_veal, basestring):
            return escape(_veal)
        return _veal
    except SyntaxError as e:
        pass
    return v
