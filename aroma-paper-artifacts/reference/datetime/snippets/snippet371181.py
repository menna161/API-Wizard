import copy
import io
import itertools
import json
import os.path
import string
from datetime import datetime
from atp.httprunner import exceptions, logger
from atp.httprunner.compat import OrderedDict, basestring, is_py2


def get_python2_retire_msg():
    retire_day = datetime(2020, 1, 1)
    today = datetime.now()
    left_days = (retire_day - today).days
    if (left_days > 0):
        retire_msg = 'Python 2 will retire in {} days, why not move to Python 3?'.format(left_days)
    else:
        retire_msg = 'Python 2 has been retired, you should move to Python 3.'
    return retire_msg
