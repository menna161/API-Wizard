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


def append(self, objs, axis: str='rows', *args, **kwargs):
    "\n        Append new rows or columns to the DataFrame.\n\n        Parameters\n        ----------\n        objs: Dictionary, DataFrame, or list of DataFrames\n            Only columns may be appended when a dictionary is used. The keys\n            must be the strings of new column names and the values must either be a\n            callable, a scalar, an array, or DataFrame. If the value of the dictionary\n            is a callable, the *args, and **kwargs are passed to it. It must return a scalar,\n            an array of a DataFrame\n\n            If a list of DataFrames is passed\n\n        axis: 'rows' or 'columns'\n\n        args: passed to\n        kwargs\n\n        Returns\n        -------\n\n        "
    axis_int: int = utils.convert_axis_string(axis)
    if isinstance(objs, dict):
        if (axis_int == 0):
            raise NotImplementedError('Using a dictionary of strings mapped to functions is only available for adding columns')
        for (k, v) in objs.items():
            if (not isinstance(k, str)):
                raise TypeError('The keys of the `objs` dict must be a string')
        n = self.shape[0]
        appended_data = {}
        df_new = self.copy()
        for (col_name, func) in objs.items():
            if isinstance(func, Callable):
                result = func(self, *args, **kwargs)
            else:
                result = func
            dtype = _va.get_kind(result)
            if (dtype == ''):
                if isinstance(result, DataFrame):
                    if (result.size == 1):
                        dtype = list(result._data.keys())[0]
                        arr = np.repeat(result[(0, 0)], n)
                    elif (result.shape[1] != 1):
                        raise ValueError(f'Returned DataFrame from function mapped from {col_name} did not return a single column DataFrame')
                    else:
                        dtype = list(result._data.keys())[0]
                        arr = result._data[dtype]
                elif isinstance(result, ndarray):
                    if (result.size == 1):
                        dtype = result.dtype.kind
                        np.repeat(result.flat[0], n)
                    elif (((result.ndim == 2) and (result.shape[1] != 1)) or (result.ndim > 2)):
                        raise ValueError('Your returned array must have only one column')
                    else:
                        dtype = result.dtype.kind
                        arr = result
                else:
                    raise TypeError(f'The return type from the function mapped from column {col_name} was not a scalar, DataFrame, or array')
            else:
                arr = np.repeat(result, n)
            if (len(arr) < n):
                arr_old = arr
                if (dtype in 'ifb'):
                    arr = np.full((n, 1), nan, dtype='float64')
                elif (dtype == 'M'):
                    arr = np.full((n, 1), NaT, dtype='datetime64[ns]')
                elif (dtype == 'm'):
                    arr = np.full((n, 1), NaT, dtype='timedelta64[ns]')
                elif (dtype == 'S'):
                    arr = np.empty((n, 1), dtype='O')
                if (arr_old.ndim == 1):
                    arr_old = arr_old[(:, np.newaxis)]
                arr[:len(arr_old)] = arr_old
            elif (len(arr) > n):
                arr = arr[:n]
            appended_data[col_name] = (dtype, arr)
        new_cols = []
        new_column_info = df_new._column_info
        new_data = df_new._data
        extra_cols = 0
        for (col_name, (dt, arr)) in appended_data.items():
            if (col_name in new_column_info):
                (old_dtype, loc, order) = self._get_col_dtype_loc_order(col_name)
                if (old_dtype == dt):
                    new_data[old_dtype][(:, loc)] = arr
                else:
                    new_data[old_dtype] = np.delete(new_data[old_dtype], loc, 1)
                    new_loc = new_data[dt].shape[1]
                    new_data[dt] = np.column_stack((new_data[dt], arr))
                    new_column_info[col_name] = utils.Column(dt, new_loc, order)
            else:
                loc = new_data[dt].shape[1]
                new_column_info[col_name] = utils.Column(dt, loc, (self.shape[1] + extra_cols))
                extra_cols += 1
                new_data[dt] = np.column_stack((new_data[dt], arr))
                new_cols.append(col_name)
        new_columns = np.append(self._columns, new_cols)
    elif isinstance(objs, (DataFrame, list)):
        if isinstance(objs, DataFrame):
            objs = [self, objs]
        else:
            objs = ([self] + objs)
        for obj in objs:
            if (not isinstance(obj, DataFrame)):
                raise TypeError('`Each item in the `objs` list must be a DataFrame`')

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
        if (axis_int == 0):
            ncs = []
            nrs = []
            total = 0
            for obj in objs:
                ncs.append(obj.shape[1])
                total += len(obj)
                nrs.append(total)
            nc = max(ncs)
            nr = nrs[(- 1)]
            new_column_info = {}
            new_columns = []
            data_pieces = defaultdict(list)
            loc_count = defaultdict(int)
            final_col_dtypes = []
            for i in range(nc):
                col_dtype = set()
                piece = []
                has_appended_column = False
                for (ncol, obj) in zip(ncs, objs):
                    if (i < ncol):
                        col = obj._columns[i]
                        if (not has_appended_column):
                            has_appended_column = True
                            new_columns.append(col)
                        (dtype, loc) = obj._get_col_dtype_loc(col)
                        col_dtype.add(dtype)
                        piece.append(obj._data[dtype][(:, loc)])
                    else:
                        piece.append(None)
                        col_dtype.add(None)
                dtype = get_final_dtype(col_dtype)
                final_col_dtypes.append(dtype)
                data_pieces[dtype].append(piece)
                loc = loc_count[dtype]
                new_column_info[new_columns[(- 1)]] = utils.Column(dtype, loc, i)
                loc_count[dtype] += 1
            new_data = {}
            for (dtype, pieces) in data_pieces.items():
                make_fast_empty = True
                for piece in pieces:
                    for p in piece:
                        if (p is None):
                            make_fast_empty = False
                            break
                ct = len(pieces)
                if (dtype in 'bi'):
                    dtype_word = utils.convert_kind_to_numpy(dtype)
                    new_data[dtype] = np.empty((nr, ct), dtype=dtype_word, order='F')
                elif (dtype == 'f'):
                    if make_fast_empty:
                        new_data[dtype] = np.empty((nr, ct), dtype='float64', order='F')
                    else:
                        new_data[dtype] = np.full((nr, ct), nan, dtype='float64', order='F')
                elif (dtype == 'S'):
                    new_data[dtype] = np.empty((nr, ct), dtype='O', order='F')
                elif (dtype == 'm'):
                    if make_fast_empty:
                        new_data[dtype] = np.empty((nr, ct), dtype='timedelta64[ns]', order='F')
                    else:
                        new_data[dtype] = np.full((nr, ct), NaT, dtype='timedelta64[ns]', order='F')
                elif (dtype == 'M'):
                    if make_fast_empty:
                        new_data[dtype] = np.empty((nr, ct), dtype='datetime64[ns]', order='F')
                    else:
                        new_data[dtype] = np.full((nr, ct), NaT, dtype='datetime64[ns]', order='F')
                for (loc, piece) in enumerate(pieces):
                    for (i, p) in enumerate(piece):
                        if (p is None):
                            continue
                        if (i == 0):
                            left = 0
                        else:
                            left = nrs[(i - 1)]
                        right = nrs[i]
                        new_data[dtype][(left:right, loc)] = p
            new_columns = np.array(new_columns, dtype='O')
        else:
            ncs = []
            nrs = []
            total = 0
            col_maps = []
            new_columns = []
            col_set = set()
            for obj in objs:
                total += obj.shape[1]
                ncs.append(total)
                nrs.append(len(obj))
                col_map = {}
                for col in obj._columns:
                    new_col = col
                    i = 1
                    while (new_col in col_set):
                        new_col = ((col + '_') + str(i))
                        i += 1
                    col_map[col] = new_col
                    col_set.add(new_col)
                    new_columns.append(new_col)
                col_maps.append(col_map)
            nc = nrs[(- 1)]
            nr = max(nrs)
            new_column_info = {}
            data_dict = defaultdict(list)
            loc_count = defaultdict(int)
            new_column_info = {}
            new_data = {}
            i = 0
            for (nrow, obj, col_map) in zip(nrs, objs, col_maps):
                for (col, dtype, loc, col_arr) in obj._col_info_iter(with_arr=True):
                    if ((nrow < nr) and (dtype in 'bi')):
                        dtype = 'f'
                    loc = len(data_dict[dtype])
                    data_dict[dtype].append(col_arr)
                    new_column_info[col_map[col]] = utils.Column(dtype, loc, i)
                    i += 1
            for (dtype, data) in data_dict.items():
                if (dtype == 'b'):
                    new_data[dtype] = np.empty((nr, len(data)), dtype='bool', order='F')
                elif (dtype == 'i'):
                    new_data[dtype] = np.empty((nr, len(data)), dtype='int64', order='F')
                elif (dtype == 'f'):
                    new_data[dtype] = np.full((nr, len(data)), nan, dtype='float64', order='F')
                elif (dtype == 'S'):
                    new_data[dtype] = np.empty((nr, len(data)), dtype='O', order='F')
                elif (dtype == 'm'):
                    new_data[dtype] = np.full((nr, len(data)), NaT, dtype='timedelta64[ns]', order='F')
                elif (dtype == 'M'):
                    new_data[dtype] = np.full((nr, len(data)), NaT, dtype='datetime64[ns]', order='F')
                for (i, arr) in enumerate(data):
                    new_data[dtype][(:len(arr), i)] = arr
            new_columns = np.array(new_columns, dtype='O')
    else:
        raise TypeError(f'`objs` must be either a dictionary, a DataFrame or a list of DataFrames. You passed in a {type(objs).__name__}')
    return self._construct_from_new(new_data, new_column_info, new_columns)
