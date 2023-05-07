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


def fillna(self, values: Union[(Scalar, Dict[(str, Scalar)], None)]=None, method: Optional[str]=None, limit: Optional[int]=None, fill_function: Optional[str]=None) -> 'DataFrame':
    "\n\n        Parameters\n        ----------\n        values: number, string or  dictionary of column name to fill value\n        method : {'bfill', 'ffill'}\n        limit : positive integer\n        fill_function : {'mean', 'median'}\n\n        Returns\n        -------\n\n        "
    if (values is not None):
        if (method is not None):
            raise ValueError('You cannot specify both `values` and and a `method` at the same time')
        if (fill_function is not None):
            raise ValueError('You cannot specify both `values` and `fill_function` at the same time')
    if (limit is not None):
        if ((not isinstance(limit, int)) or (limit < 1)):
            raise ValueError('`limit` must be a positive integer')
    else:
        limit = len(self)
    if (isinstance(values, (int, float, np.number)) and (not isinstance(values, np.timedelta64))):
        if self._is_string():
            raise TypeError('Your DataFrame contains only str columns and you are trying to pass a number to fill in missing values')
        if self._is_date():
            raise TypeError('Your DataFrame contains only datetime/timedelta columns and you are trying to pass a number to fill in missing values')
        new_data: Dict[(str, ndarray)] = {}
        for (dtype, arr) in self._data.items():
            arr = arr.copy('F')
            if (dtype == 'f'):
                if (limit >= len(self)):
                    new_data['f'] = np.where(np.isnan(arr), values, arr)
                else:
                    for col in self._columns:
                        (dtype2, loc, _) = self._column_info[col].values
                        if (dtype2 == 'f'):
                            col_arr = arr[(:, loc)]
                            idx: ndarray = np.where(np.isnan(col_arr))[0][:limit]
                            col_arr[idx] = values
                    new_data['f'] = arr
            else:
                new_data[dtype] = arr
    elif isinstance(values, str):
        if ('S' not in self._data):
            raise TypeError("You passed a `str` value to the `values` parameter. You're DataFrame contains no str columns.")
        new_data = {}
        for (dtype, arr) in self._data.items():
            arr = arr.copy('F')
            if (dtype == 'S'):
                for col in self._columns:
                    (dtype2, loc, _) = self._column_info[col].values
                    if (dtype2 == 'S'):
                        col_arr = arr[(:, loc)]
                        na_arr: ndarray = _math.isna_str_1d(col_arr)
                        idx = np.where(na_arr)[0][:limit]
                        col_arr[idx] = values
                new_data['S'] = arr
            else:
                new_data[dtype] = arr
    elif isinstance(values, np.datetime64):
        if ('M' not in self._data):
            raise TypeError('You passed a `datetime64` value to the `values` parameter but your DataFrame contains no datetime64 columns')
        new_data = {}
        for (dtype, arr) in self._data.items():
            arr = arr.copy('F')
            if (dtype == 'M'):
                for col in self._columns:
                    (dtype2, loc, _) = self._column_info[col].values
                    if (dtype2 == 'M'):
                        col_arr = arr[(:, loc)]
                        na_arr: ndarray = np.isnat(col_arr)
                        idx = np.where(na_arr)[0][:limit]
                        col_arr[idx] = values.astype('datetime64[ns]')
                new_data['M'] = arr
            else:
                new_data[dtype] = arr
    elif isinstance(values, np.timedelta64):
        if ('m' not in self._data):
            raise TypeError('You passed a `timedelta64` value to the `values` parameter but your DataFrame contains no timedelta64 columns')
        new_data = {}
        for (dtype, arr) in self._data.items():
            arr = arr.copy('F')
            if (dtype == 'm'):
                for col in self._columns:
                    (dtype2, loc, _) = self._column_info[col].values
                    if (dtype2 == 'm'):
                        col_arr = arr[(:, loc)]
                        na_arr: ndarray = np.isnat(col_arr)
                        idx = np.where(na_arr)[0][:limit]
                        col_arr[idx] = values.astype('timedelta64[ns]')
                new_data['m'] = arr
            else:
                new_data[dtype] = arr
    elif isinstance(values, dict):
        self._validate_column_name_list(list(values))
        dtype_locs: Dict[(str, List[Tuple[(str, int, Scalar)]])] = defaultdict(list)
        for (col, val) in values.items():
            (dtype, loc) = self._get_col_dtype_loc(col)
            if (dtype in 'fO'):
                dtype_locs[dtype].append((col, loc, val))
        for (col, loc, new_val) in dtype_locs['f']:
            if (not isinstance(new_val, (int, float, np.number))):
                raise TypeError(f'Column {col} has dtype float. Must set with a number')
        for (col, loc, new_val) in dtype_locs['S']:
            if (not isinstance(new_val, str)):
                raise TypeError(f'Column {col} has dtype {dtype}. Must set with a str')
        arr_float: ndarray = self._data.get('f', []).copy('F')
        arr_str: ndarray = self._data.get('S', []).copy('F')
        for (col, loc, new_val) in dtype_locs['f']:
            if (limit >= len(self)):
                arr_float[(:, loc)] = np.where(np.isnan(arr_float[(:, loc)]), new_val, arr_float[(:, loc)])
            else:
                idx = np.where(np.isnan(arr_float[(:, loc)]))[0][:limit]
                arr_float[(idx, loc)] = new_val
        for (col, loc, new_val) in dtype_locs['S']:
            na_arr = _math.isna_str_1d(arr_str[(:, loc)])
            if (limit >= len(self)):
                arr_str[(:, loc)] = np.where(na_arr, new_val, arr_str[(:, loc)])
            else:
                idx = np.where(na_arr)[0][:limit]
                arr_float[(idx, loc)] = new_val
        new_data = {}
        for (dtype, arr) in self._data.items():
            if (dtype == 'f'):
                new_data[dtype] = arr_float
            elif (dtype == 'S'):
                new_data[dtype] = arr_str
            else:
                new_data[dtype] = arr.copy('F')
    elif (values is None):
        if ((method is None) and (fill_function is None)):
            raise ValueError('One of `values`, `method`, or `fill_function` must not be None')
        if (method is not None):
            if (fill_function is not None):
                raise ValueError('You cannot specify both `method` and `fill_function` at the same time')
            if (method == 'ffill'):
                new_data = {}
                for (dtype, arr) in self._data.items():
                    arr = arr.copy('F')
                    if (dtype == 'f'):
                        new_data['f'] = _math.ffill_float(arr, limit)
                    elif (dtype == 'S'):
                        new_data['S'] = _math.ffill_str(arr, limit)
                    elif (dtype in 'mM'):
                        nans = np.isnat(arr)
                        dtype_name = ('datetime64[ns]' if (dtype == 'M') else 'timedelta64[ns]')
                        new_data[dtype] = _math.ffill_date(arr.view('int64'), limit, nans).astype(dtype_name)
                    else:
                        new_data[dtype] = arr
            elif (method == 'bfill'):
                new_data = {}
                for (dtype, arr) in self._data.items():
                    arr = arr.copy('F')
                    if (dtype == 'f'):
                        new_data['f'] = _math.bfill_float(arr, limit)
                    elif (dtype == 'S'):
                        new_data['S'] = _math.bfill_str(arr, limit)
                    elif (dtype in 'mM'):
                        nans = np.isnat(arr)
                        dtype_name = ('datetime64[ns]' if (dtype == 'M') else 'timedelta64[ns]')
                        new_data[dtype] = _math.bfill_date(arr.view('int64'), limit, nans).astype(dtype_name)
                    else:
                        new_data[dtype] = arr
            else:
                raise ValueError('`method` must be either "bfill" or "ffill"')
        else:
            if (fill_function not in ['mean', 'median']):
                raise ValueError('`fill_function` must be either "mean" or "median"')
            new_data = {}
            for (dtype, arr) in self._data.items():
                arr = arr.copy('F')
                if (dtype == 'f'):
                    fill_vals = getattr(self, fill_function)().values
                    new_data['f'] = np.where(np.isnan(arr), fill_vals, arr)
                else:
                    new_data[dtype] = arr
    else:
        raise TypeError(f'`values` must be either an int, str, dict or None. You passed {values}')
    new_columns = self._columns.copy()
    new_column_info = self._copy_column_info()
    return self._construct_from_new(new_data, new_column_info, new_columns)
