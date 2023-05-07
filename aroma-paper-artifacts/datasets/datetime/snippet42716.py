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


def get_final_dtype(col_dtype):
    if ((len(col_dtype) == 1) or ((len(col_dtype) == 2) and (None in col_dtype) and ('i' not in col_dtype) and ('b' not in col_dtype))):
        return next(iter((col_dtype - {None})))
    elif ('m' in col_dtype):
        raise TypeError(f'The DataFrames that you are appending togethere have a timedelta64[ns] column and another type in column number {i}. When appending timedelta64[ns], all columns must have that type.')
    elif ('M' in col_dtype):
        raise TypeError(f'The DataFrames that you are appending togethere have a datetime64[ns] column and another type in column number {i}. When appending datetime64[ns], all columns must have that type.')
    elif ('S' in col_dtype):
        raise TypeError('You are trying to append a string column with a non-string column. Both columns must be strings.')
    elif (('f' in col_dtype) or (None in col_dtype)):
        return 'f'
    elif ('i' in col_dtype):
        return 'i'
    else:
        raise ValueError('This error should never happen.')
