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
def toDate(value: Any) -> Optional[float]:
    '\n    Coerces the input value to a Date instance.\n    Null values and empty strings are mapped to null.\n    If an optional parser function is provided, it is used to\n    perform date parsing, otherwise Date.parse is used.\n    '
    if isinstance(value, (float, int)):
        return value
    if ((value is None) or (value == '')):
        return None
    return (pd.to_datetime(value).timestamp() * 1000)
