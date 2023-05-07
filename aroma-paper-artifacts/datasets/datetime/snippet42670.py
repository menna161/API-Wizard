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


def sort_values(self, by: Union[(str, List[str])], axis: str='rows', ascending: Union[(bool, List[bool])]=True) -> 'DataFrame':
    axis_num = utils.convert_axis_string(axis)
    if (axis_num == 1):
        raise NotImplementedError('Not implemented for sorting rows')
    if isinstance(by, str):
        self._validate_column_name(by)
        by = [by]
    elif isinstance(by, list):
        self._validate_column_name_list(by)
    else:
        raise TypeError('`by` variable must either be a column name as a string or a list of column names as strings')
    if isinstance(ascending, list):
        if (len(ascending) != len(by)):
            raise ValueError(f'The number of columns in `by` does not match the number of booleans in `ascending` list {len(by)} != {len(ascending)}')
        for asc in ascending:
            if (not isinstance(asc, bool)):
                raise TypeError('All values passed to `ascending` list must be boolean')
    elif (not isinstance(ascending, bool)):
        raise TypeError('`ascending` must be a boolean or list of booleans')
    else:
        ascending = ([ascending] * len(by))
    if (len(by) == 1):
        col = by[0]
        (dtype, loc) = self._get_col_dtype_loc(col)
        col_arr = self._data[dtype][(:, loc)]
        hasnans: ndarray = self._hasnans.get(col, True)
        asc = ascending[0]
        col_arr = self._replace_nans(dtype, col_arr, asc, hasnans)
        count_sort: bool = False
        if (dtype == 'S'):
            if ((len(col_arr) > 1000) and (len(set(np.random.choice(col_arr, 100))) <= 70)):
                d: ndarray = _sr.sort_str_map(col_arr, asc)
                arr: ndarray = _sr.replace_str_int(col_arr, d)
                counts: ndarray = _sr.count_int_ordered(arr, len(d))
                new_order: ndarray = _sr.get_idx(arr, counts)
                count_sort = True
            else:
                col_arr = col_arr.astype('U')
                if asc:
                    new_order = np.argsort(col_arr, kind='mergesort')
                else:
                    new_order = np.argsort(col_arr[::(- 1)], kind='mergesort')
        elif asc:
            new_order = np.argsort(col_arr, kind='mergesort')
        else:
            new_order = np.argsort(col_arr[::(- 1)], kind='mergesort')
        new_data: Dict[(str, ndarray)] = {}
        for (dtype, arr) in self._data.items():
            np_dtype = utils.convert_kind_to_numpy(dtype)
            arr_final = np.empty(arr.shape, dtype=np_dtype, order='F')
            for i in range(arr.shape[1]):
                if (asc or count_sort):
                    arr_final[(:, i)] = arr[(:, i)][new_order]
                else:
                    arr_final[(:, i)] = arr[(::(- 1), i)][new_order[::(- 1)]]
            new_data[dtype] = arr_final
        new_column_info = self._copy_column_info()
        new_columns = self._columns.copy()
        return self._construct_from_new(new_data, new_column_info, new_columns)
    else:
        single_cols: List[ndarray] = []
        for (col, asc) in zip(by, ascending):
            (dtype, loc) = self._get_col_dtype_loc(col)
            col_arr = self._data[dtype][(:, loc)]
            hasnans = self._hasnans.get(col, True)
            col_arr = self._replace_nans(dtype, col_arr, asc, hasnans)
            if (not asc):
                if (dtype == 'b'):
                    col_arr = (~ col_arr)
                elif (dtype == 'S'):
                    d = _sr.sort_str_map(col_arr, asc)
                    col_arr = _sr.replace_str_int(col_arr, d)
                elif (dtype == 'M'):
                    col_arr = (- (col_arr.view('int64') + 1)).astype('datetime64[ns]')
                elif (dtype == 'm'):
                    col_arr = (- (col_arr.view('int64') + 1)).astype('timedelta64[ns]')
                else:
                    col_arr = (- col_arr)
            elif (dtype == 'S'):
                if ((len(col_arr) > 1000) and (len(set(np.random.choice(col_arr, 100))) <= 70)):
                    d = _sr.sort_str_map(col_arr, asc)
                    col_arr = _sr.replace_str_int(col_arr, d)
                else:
                    col_arr = col_arr.astype('U')
            single_cols.append(col_arr)
        new_order = np.lexsort(single_cols[::(- 1)])
    new_data = {}
    for (dtype, arr) in self._data.items():
        np_dtype = utils.convert_kind_to_numpy(dtype)
        arr_final = np.empty(arr.shape, dtype=np_dtype, order='F')
        for i in range(arr.shape[1]):
            arr_final[(:, i)] = arr[(:, i)][new_order]
        new_data[dtype] = arr_final
    new_column_info = self._copy_column_info()
    new_columns = self._columns.copy()
    return self._construct_from_new(new_data, new_column_info, new_columns)
