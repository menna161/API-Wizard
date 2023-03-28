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
def quarter(datetime: dt.datetime) -> int:
    '\n    Returns the quarter of the year (0-3) for the given datetime value,\n    in local time.\n    '
    return ((datetime.month - 1) // 3)
