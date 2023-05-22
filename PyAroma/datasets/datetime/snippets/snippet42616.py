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


def _setitem_change_dtype(self, value, dtype: str, loc: int, col_name: str):
    is_bool = isinstance(value, (bool, np.bool_))
    is_int = isinstance(value, (int, np.integer))
    is_float = isinstance(value, (float, np.floating))
    is_dt = isinstance(value, np.datetime64)
    is_td = isinstance(value, np.timedelta64)
    is_str = isinstance(value, (bytes, str))
    is_nan = (is_float and np.isnan(value))
    is_none = (value is None)
    bad_type = False
    if (dtype == 'b'):
        if is_bool:
            value = int(value)
        elif (is_nan or is_none):
            value = (- 1)
        elif is_int:
            self._astype_internal(col_name, 'int64')
        elif (is_float and (not np.isnan(value))):
            self._astype_internal(col_name, 'float64')
        else:
            bad_type = True
    elif (dtype == 'i'):
        if is_int:
            pass
        elif (is_nan or is_none):
            value = MIN_INT
        elif is_float:
            self._astype_internal(col_name, 'float64')
        else:
            bad_type = True
    elif (dtype == 'f'):
        if (not (is_float or is_int or is_bool or is_none)):
            bad_type = True
    elif (dtype == 'M'):
        if (not is_dt):
            bad_type = True
    elif (dtype == 'm'):
        if (not is_td):
            bad_type = True
    elif (dtype == 'S'):
        if (is_nan or is_none):
            value = False
        elif (not is_str):
            bad_type = True
    if bad_type:
        raise TypeError(f'Cannot set column {col_name} which has type {utils._DT[dtype]} with type {type(value)}')
    return value
