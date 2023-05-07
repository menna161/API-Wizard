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


def isin(self, values: Union[(Scalar, List[Scalar], Dict[(str, Union[(Scalar, List[Scalar])])])]) -> 'DataFrame':
    if utils.is_scalar(values):
        values = [values]

    def separate_value_types(vals: List[Scalar]) -> Tuple[(List[Union[(float, int, bool)]], List[str])]:
        val_numbers = []
        val_strings = []
        val_datetimes = []
        val_timedeltas = []
        for val in vals:
            if isinstance(val, np.datetime64):
                val_datetimes.append(val)
            elif isinstance(val, np.timedelta64):
                val_timedeltas.append(val)
            elif isinstance(val, (float, int, np.number)):
                val_numbers.append(val)
            elif isinstance(val, str):
                val_strings.append(val)
        return (val_numbers, val_strings, val_datetimes, val_timedeltas)
    if isinstance(values, list):
        for value in values:
            if (not utils.is_scalar(value)):
                raise ValueError('All values in list must be either int, float, str, or bool')
        arrs: List[ndarray] = []
        (val_numbers, val_strings, val_datetimes, val_timedeltas) = separate_value_types(values)
        dtype_add = {}
        for (dtype, arr) in self._data.items():
            dtype_add[dtype] = utils.get_num_cols(arrs)
            if (dtype == 'S'):
                arrs.append(np.isin(arr, val_strings))
            elif (dtype == 'M'):
                arrs.append(np.isin(arr, val_datetimes))
            elif (dtype == 'm'):
                arrs.append(np.isin(arr, val_timedeltas))
            else:
                arrs.append(np.isin(arr, val_numbers))
        new_column_info = {}
        for (col, dtype, loc, order) in self._col_info_iter(with_order=True):
            new_column_info[col] = utils.Column('b', (loc + dtype_add[dtype]), order)
        new_columns = self._columns.copy()
        new_data = {'b': np.asfortranarray(np.column_stack(arrs))}
        return self._construct_from_new(new_data, new_column_info, new_columns)
    elif isinstance(values, dict):
        self._validate_column_name_list(list(values))
        arr_final = np.full(self.shape, False, dtype='bool')
        for (col, vals) in values.items():
            if utils.is_scalar(vals):
                vals = [vals]
            if (not isinstance(vals, list)):
                raise TypeError('The dictionary values must be lists or a scalar')
            (dtype, loc, order) = self._get_col_dtype_loc_order(col)
            col_arr = self._data[dtype][(:, loc)]
            (val_numbers, val_strings, val_datetimes, val_timedeltas) = separate_value_types(vals)
            if (dtype == 'S'):
                arr_final[(:, order)] = np.isin(col_arr, val_strings)
            elif (dtype == 'M'):
                arr_final[(:, order)] = np.isin(col_arr, val_datetimes)
            elif (dtype == 'm'):
                arr_final[(:, order)] = np.isin(col_arr, val_timedeltas)
            else:
                arr_final[(:, order)] = np.isin(col_arr, val_numbers)
        new_data = {'b': arr_final}
        new_columns = self._columns.copy()
        new_column_info = {}
        for (i, col) in enumerate(self._columns):
            new_column_info[col] = utils.Column('b', i, i)
        return self._construct_from_new(new_data, new_column_info, new_columns)
    else:
        raise TypeError('`values` must be a scalar, list, or dictionary of scalars/lists')
