from collections import defaultdict
from math import ceil
from copy import deepcopy
from typing import Union, Dict, List, Optional, Tuple, Callable, overload, NoReturn, Set, Iterable, Any, TypeVar, Type, Generator
import warnings
import numpy as np
from numpy import nan, ndarray
from . import _init_funcs as init
from . import _utils as utils
from . import options
from ._date import DateTimeClass, TimeDeltaClass
from ._libs import groupby as _gb, validate_arrays as _va, math as _math, math_oper_string as _mos, sort_rank as _sr, unique as _uq, replace as _repl, pivot as _pivot, out_files as _of, join as _join
from ._strings import StringClass
from . import _stat_funcs as _sf
from ._arithmetic_ops import Operations2D
from ._libs import math_oper
from ._groupby import Grouper
from ._rolling import Roller


def separate_value_types(vals: List[Scalar]) -> Tuple[(List[Union[(float, int, bool)]], List[str])]:
    val_numbers = []
    val_strings = []
    val_datetimes = []
    val_timedeltas = []
    for val in vals:
        if isinstance(val, np.datetime64):
            val_datetimes.append(val)
        elif isinstance(val, np.timedelta64):
            val_timedeltas.append(val)
        elif isinstance(val, (float, int, np.number)):
            val_numbers.append(val)
        elif isinstance(val, str):
            val_strings.append(val)
    return (val_numbers, val_strings, val_datetimes, val_timedeltas)
