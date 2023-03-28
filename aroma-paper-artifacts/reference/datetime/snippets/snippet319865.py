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
def utc(year: int, month: int=0, day: int=1, hour: int=0, min: int=0, sec: int=0, millisec: int=0) -> float:
    '\n    Returns a timestamp for the given UTC date.\n    The month is 0-based, such that 1 represents February.\n    '
    return (dt.datetime(int(year), (int(month) + 1), int(day), int(hour), int(min), int(sec), int((millisec * 1000)), tzinfo=dt.timezone.utc).timestamp() * 1000)
