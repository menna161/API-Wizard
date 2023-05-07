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


def streak(self, column: Optional[str]=None, value: Optional[Scalar]=None, group: bool=False) -> ndarray:
    '\n        Three types of streaks for a single column. Must specify Column\n        All values - begin at 1, value=None\n        Specific value given by value\n        group - each group is given same number\n        '
    if (not isinstance(column, str)):
        raise TypeError('`column` must be a column name as a string')
    else:
        self._validate_column_name(column)
    if (not isinstance(group, (bool, np.bool_))):
        raise TypeError('`group` must be either True or False')
    (dtype, loc) = self._get_col_dtype_loc(column)
    col_arr = self._data[dtype][(:, loc)]
    if (not group):
        if (value is None):
            func_name = ('streak_' + utils.convert_kind_to_dtype_generic(dtype))
            func = getattr(_math, func_name)
            if (dtype in 'mM'):
                return func(col_arr.view('int64'))
            else:
                return func(col_arr)
        elif (dtype == 'i'):
            if (not isinstance(value, (int, np.integer))):
                raise TypeError(f'Column {column} has dtype int and `value` is a {type(value).__name__}.')
            return _math.streak_value_int(col_arr, value)
        elif (dtype == 'f'):
            if (not isinstance(value, (int, float, np.number))):
                raise TypeError(f'Column {column} has dtype float and `value` is a {type(value).__name__}.')
            return _math.streak_value_float(col_arr, value)
        elif (dtype == 'S'):
            if (not isinstance(value, str)):
                raise TypeError(f'Column {column} has dtype str and `value` is a {type(value).__name__}.')
            return _math.streak_value_str(col_arr, value)
        elif (dtype == 'b'):
            if (not isinstance(value, (bool, np.bool_))):
                raise TypeError(f'Column {column} has dtype bool and `value` is a {type(value).__name__}.')
            return _math.streak_value_bool(col_arr, value)
        elif (dtype == 'M'):
            if (not isinstance(value, np.datetime64)):
                raise TypeError(f'Column {column} has dtype datetime64 and `value` is a {type(value).__name__}.')
            return _math.streak_value_int(col_arr.view('int64'), value.astype('int64'))
        elif (dtype == 'm'):
            if (not isinstance(value, np.timedelta64)):
                raise TypeError(f'Column {column} has dtype timedelta64 and `value` is a {type(value).__name__}.')
            value = value.astype('timedelta64[ns]').astype('int64')
            return _math.streak_value_int(col_arr.view('int64'), value)
    else:
        if (value is not None):
            raise ValueError('If `group` is True then `value` must be None')
        func_name = ('streak_group_' + utils.convert_kind_to_dtype_generic(dtype))
        func = getattr(_math, func_name)
        if (dtype in 'mM'):
            col_arr = col_arr.view('int64')
        return func(col_arr)
