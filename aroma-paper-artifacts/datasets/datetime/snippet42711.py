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


def check_to_replace_type(key, col, col_dtype):
    keys = key
    if (not isinstance(keys, tuple)):
        keys = (keys,)
    for key in keys:
        if ((col_dtype == 'b') and (not isinstance(key, (bool, np.bool_)))):
            raise ValueError(f'Column "{col}" is boolean and you are trying to replace {key}, which is of type {type(key)}')
        elif ((col_dtype == 'i') and (not isinstance(key, (bool, np.bool_, int, np.integer)))):
            raise ValueError(f'Column "{col}" is an int and you are trying to replace {key}, which is of type {type(key)}')
        elif ((col_dtype == 'f') and (not isinstance(key, (bool, np.bool_, int, np.integer, float, np.floating)))):
            raise ValueError(f'Column "{col}" is a float and you are trying to replace {key}, which is of type {type(key)}')
        elif ((col_dtype == 'S') and (not isinstance(key, str))):
            raise ValueError(f'Column "{col}" is a str and you are trying to replace {key}, which is of type {type(key)}')
        elif ((col_dtype == 'M') and (not isinstance(key, np.datetime64))):
            raise ValueError(f'Column "{col}" is a datetime64 and you are trying to replace {key}, which is of type {type(key)}')
        elif ((col_dtype == 'm') and (not isinstance(key, np.timedelta64))):
            raise ValueError(f'Column "{col}" is a timedelta64 and you are trying to replace {key}, which is of type {type(key)}')
