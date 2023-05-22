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


def melt(self, id_vars=None, value_vars=None, var_name='variable', value_name='value'):

    def check_string_or_list(vals, name, none_possible=True):
        if isinstance(vals, str):
            return [vals]
        elif isinstance(vals, list):
            return vals
        elif isinstance(vals, np.ndarray):
            return vals.tolist()
        elif ((vals is None) and none_possible):
            return []
        else:
            raise TypeError('`{name}` must be a string or list of strings')
    id_vars = check_string_or_list(id_vars, 'id_vars')
    value_vars = check_string_or_list(value_vars, 'value_vars')
    var_name = check_string_or_list(var_name, 'var_name', False)
    value_name = check_string_or_list(value_name, 'value_name', False)
    if id_vars:
        self._validate_column_name_list(id_vars)
    id_vars_set = set(id_vars)
    if (value_vars == []):
        value_vars = [col for col in self._columns if (col not in id_vars_set)]
    if (not isinstance(value_vars[0], list)):
        value_vars = [value_vars]
    n_groups = len(value_vars)
    if (n_groups != len(var_name)):
        if (len(var_name) != 1):
            raise ValueError(f'Number of inner lists of value_vars must equal length of var_name {len(value_vars)} != {len(var_name)}')
        else:
            var_name = [((var_name[0] + '_') + str(i)) for i in range(n_groups)]
    for vn in var_name:
        if (not isinstance(vn, str)):
            raise TypeError('`var_name` must be a string or list of strings')
    if (n_groups != len(value_name)):
        if (len(value_name) != 1):
            raise ValueError(f'Number of inner lists of value_vars must equal length of value_name {n_groups} != {len(value_name)}')
        else:
            value_name = [((value_name[0] + '_') + str(i)) for i in range(n_groups)]
    for vv in value_name:
        if (not isinstance(vv, str)):
            raise TypeError('`value_name` must be a string or list of strings')
    value_vars_length = [len(vv) for vv in value_vars]
    max_group_len = max(value_vars_length)
    data_dict = defaultdict(list)
    new_column_info = {}
    col_set = set(self._columns)
    if (len(id_vars_set) != len(id_vars)):
        raise ValueError('`id_vars` cannot contain duplicate column names')
    all_value_vars_set = set()
    for vv in value_vars:
        for col in vv:
            if (col in id_vars_set):
                raise ValueError(f'Column "{col}" cannot be both an id_var and a value_var')
            if (col in all_value_vars_set):
                raise ValueError(f'column "{col}" is already a value_var')
            self._validate_column_name(col)
            all_value_vars_set.add(col)
    cur_order = 0
    new_columns = []
    for (i, col) in enumerate(id_vars):
        (dtype, loc) = self._get_col_dtype_loc(col)
        arr = self._data[dtype][(:, loc)]
        arr = np.tile(arr, max_group_len)
        new_loc = len(data_dict[dtype])
        data_dict[dtype].append(arr)
        new_column_info[col] = utils.Column(dtype, new_loc, i)
        cur_order += 1
        new_columns.append(col)
    vars_zipped = zip(value_vars, var_name, value_name, value_vars_length)
    fill_empty_arr = {}
    for (i, (val_v, var_n, val_n, vvl)) in enumerate(vars_zipped):
        dtype_loc = defaultdict(list)
        for col in val_v:
            (dtype, loc) = self._get_col_dtype_loc(col)
            dtype_loc[dtype].append(loc)
        if (len(dtype_loc) > 1):
            dt_string = ''
            if ('S' in dtype_loc):
                dt_string = 'string'
            elif ('m' in dtype_loc):
                dt_string = 'timedelta'
            elif ('M' in dtype_loc):
                dt_string = 'datetime'
            elif ('f' in dtype_loc):
                new_dtype = 'f'
            elif ('i' in dtype_loc):
                new_dtype = 'i'
            elif ('b' in dtype_loc):
                new_dtype = 'b'
            if dt_string:
                raise TypeError(f'You are attempting to melt columns with a mix of {dt_string} and non-{dt_string} types. You can only melt string columns if they are all string columns')
        else:
            new_dtype = dtype
        if (len(val_v) < max_group_len):
            if (dtype in 'ib'):
                new_dtype = 'f'
            fill_empty_arr[new_dtype] = True
        cur_loc = len(data_dict['S'])
        variable_vals = np.repeat(np.array(val_v, dtype='O'), len(self))
        data_dict['S'].append(variable_vals)
        new_column_info[var_n] = utils.Column('S', cur_loc, cur_order)
        cur_order += 1
        new_columns.append(var_n)
        if (len(dtype_loc) == 1):
            locs = dtype_loc[dtype]
            data = self._data[dtype][(:, locs)].flatten('F')
        else:
            all_data = []
            for (dtype, loc) in dtype_loc.items():
                all_data.append(self._data[dtype][(:, loc)])
            data = np.concatenate(all_data)
        cur_loc = len(data_dict[new_dtype])
        data_dict[new_dtype].append(data)
        new_column_info[val_n] = utils.Column(new_dtype, cur_loc, cur_order)
        cur_order += 1
        new_columns.append(val_n)
    new_columns = np.array(new_columns, dtype='O')
    N = (max_group_len * len(self))
    new_data = {}
    for (dtype, data_list) in data_dict.items():
        size = (N, len(data_list))
        if fill_empty_arr.get(dtype, False):
            if (dtype == 'f'):
                arr = np.full(size, nan, dtype='float64', order='F')
            elif (dtype == 'S'):
                arr = np.empty(size, dtype='O', order='F')
            elif (dtype == 'm'):
                arr = np.full(size, NaT, dtype='timedelta64', order='F')
            elif (dtype == 'M'):
                arr = np.full(size, NaT, dtype='datetime64', order='F')
        else:
            dtype_word = utils.convert_kind_to_numpy(dtype)
            arr = np.empty(size, dtype=dtype_word, order='F')
        for (i, data) in enumerate(data_list):
            arr[(:len(data), i)] = data
        new_data[dtype] = arr
    return self._construct_from_new(new_data, new_column_info, new_columns)
