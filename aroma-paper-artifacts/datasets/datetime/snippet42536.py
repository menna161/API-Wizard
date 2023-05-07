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


@property
def values(self) -> ndarray:
    '\n        Retrieve a single 2-d array of all the data in the correct column order\n        '
    if (len(self._data) == 1):
        kind: str = next(iter(self._data))
        order: List[int] = [self._column_info[col].loc for col in self._columns]
        arr = self._data[kind][(:, order)]
        if (kind == 'b'):
            return (arr == 1)
        else:
            return arr
    if ({'b', 'S', 'm', 'M'} & self._data.keys()):
        arr_dtype: str = 'O'
    else:
        arr_dtype = 'float64'
    v: ndarray = np.empty(self.shape, dtype=arr_dtype, order='F')
    for (col, dtype, loc, order, col_arr) in self._col_info_iter(with_order=True, with_arr=True):
        if (dtype == 'S'):
            cur_list_map = self._str_reverse_map[loc]
            _va.make_object_str_array(cur_list_map, v, col_arr, order)
        elif (dtype == 'M'):
            unit = col_arr.dtype.name.replace(']', '').split('[')[1]
            _va.make_object_datetime_array(v, col_arr.view('uint64'), order, unit)
        elif (dtype == 'm'):
            unit = col_arr.dtype.name.replace(']', '').split('[')[1]
            _va.make_object_timedelta_array(v, col_arr.view('uint64'), order, unit)
        else:
            v[(:, order)] = col_arr
    return v
