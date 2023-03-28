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


@overload
def datetime(year: float, month: int, day: int=0, hour: int=0, min: int=0, sec: int=0, millisec: float=0) -> dt.datetime:
    ...
