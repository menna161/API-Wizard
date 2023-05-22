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


def get_replacement_col(col_dtype, to_repl, replace_val, col):
    if (col_dtype == 'm'):
        if (not isinstance(replace_val, np.timedelta64)):
            raise TypeError(f'Cannot replace a timedelta64 with {type(replace_val)}')
        dtype_conversion[col] = 'm'
    elif (col_dtype == 'b'):
        if isinstance(replace_val, (bool, np.bool_)):
            if (dtype_conversion.get('b', None) not in 'if'):
                dtype_conversion[col] = 'b'
        elif isinstance(replace_val, (int, np.integer)):
            if (dtype_conversion.get('b', None) != 'f'):
                dtype_conversion[col] = 'i'
        elif isinstance(replace_val, (float, np.floating)):
            dtype_conversion[col] = 'f'
        else:
            raise TypeError(f'Cannot replace a boolean with {type(replace_val)}')
    elif (col_dtype == 'i'):
        if isinstance(replace_val, (bool, np.bool_, int, np.integer)):
            dtype_conversion[col] = 'i'
        elif isinstance(replace_val, (float, np.floating)):
            dtype_conversion[col] = 'f'
        else:
            raise TypeError(f'Cannot replace an integer with {type(replace_val)}')
    elif (col_dtype == 'f'):
        if (not isinstance(replace_val, (bool, np.bool_, int, np.integer, float, np.floating))):
            raise TypeError(f'Cannot replace a float with {type(replace_val)}')
        dtype_conversion[col] = 'f'
    elif (col_dtype == 'S'):
        if ((not isinstance(replace_val, str)) and (replace_val is not None)):
            raise TypeError(f'Cannot replace a str with {type(replace_val)}')
        dtype_conversion[col] = 'S'
    elif (col_dtype == 'M'):
        if (not isinstance(replace_val, np.datetime64)):
            raise TypeError(f'Cannot replace a datetime64 with {type(replace_val)}')
        dtype_conversion[col] = 'M'
    specific_replacement[col].append((to_repl, replace_val))
