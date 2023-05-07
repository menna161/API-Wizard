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


def get_curr_var(var: Optional[ndarray], dtype: str, name: str) -> Optional[ndarray]:
    if (var is None):
        return (None if (dtype == 'S') else nan)
    types: Any
    if (dtype == 'S'):
        good_dtypes = ['S', 'U']
        types = str
    elif (dtype in 'if'):
        good_dtypes = ['i', 'f']
        types = (int, float, np.number)
    elif (dtype == 'b'):
        good_dtypes = ['b']
        types = (bool, np.bool_)
    elif (dtype == 'M'):
        good_dtypes = ['M']
        types = np.datetime64
    elif (dtype == 'm'):
        good_dtypes = ['m']
        types = np.timedelta64
    if isinstance(var, ndarray):
        var_curr = get_arr(var)
        if (var_curr.dtype.kind not in good_dtypes):
            raise TypeError(f'The array you passed to `{name}` must have compatible dtypes to the same columns in the calling DataFrame')
    elif (not isinstance(var, types)):
        raise TypeError(f'The values you are using to set with `{name}` do not have compatible types with one of the columns')
    else:
        var_curr = var
    return var_curr
