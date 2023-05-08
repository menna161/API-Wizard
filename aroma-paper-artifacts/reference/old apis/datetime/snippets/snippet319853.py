import datetime as dt
from functools import reduce, wraps
import itertools
import math
import operator
import random
import sys
import time as timemod
from typing import Any, Callable, Dict, Optional, List, Union, overload
import numpy as np
import pandas as pd
from dateutil import tz
from altair_transform.utils import evaljs, undefined, JSRegex
from scipy.stats import norm
from scipy.stats import norm
from scipy.stats import norm
from scipy.stats import norm
from scipy.stats import lognorm
from scipy.stats import lognorm
from scipy.stats import lognorm
from scipy.stats import lognorm
from scipy.stats import uniform
from scipy.stats import uniform
from scipy.stats import uniform
from scipy.stats import uniform


@vectorize
def datetime(*args):
    'Returns a new Date instance.\n\n    datetime()  # current time\n    datetime(timestamp)\n    datetime(year, month[, day, hour, min, sec, millisec])\n\n    The month is 0-based, such that 1 represents February.\n    '
    if (len(args) == 0):
        return dt.datetime.now()
    elif (len(args) == 1):
        return dt.datetime.fromtimestamp((0.001 * args[0]))
    elif (len(args) == 2):
        return dt.datetime(*args, 1)
    elif (len(args) <= 7):
        args = list(map(int, args))
        args[1] += 1
        if (len(args) == 2):
            args.append(0)
        if (len(args) == 7):
            args[6] = int((args[6] * 1000))
        return dt.datetime(*args)
    else:
        raise ValueError('Too many arguments')
