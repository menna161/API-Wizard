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


def replace(self, replace_dict):
    if (not isinstance(replace_dict, dict)):
        raise TypeError('`replace_dict` must be a dictionary')
    is_all = False
    is_one = False
    specific_replacement = defaultdict(list)
    dtype_conversion = {}

    def get_replacement(key, val):
        if isinstance(key, np.timedelta64):
            if (not isinstance(val, np.timedelta64)):
                raise TypeError(f'Cannot replace a timedelta64 with {type(val)}')
            dtype = 'm'
            dtype_conversion['m'] = 'm'
        elif isinstance(key, (bool, np.bool_)):
            if isinstance(val, (bool, np.bool_)):
                if (dtype_conversion.get('b', None) != 'f'):
                    dtype_conversion['b'] = 'b'
            elif isinstance(val, (int, np.integer)):
                if (dtype_conversion.get('b', None) != 'f'):
                    dtype_conversion['b'] = 'i'
            elif isinstance(val, (float, np.floating)):
                dtype_conversion['b'] = 'f'
            else:
                raise TypeError(f'Cannot replace a boolean with {type(val)}')
            dtype = 'b'
        elif isinstance(key, (int, np.integer)):
            if isinstance(val, (bool, np.bool_, int, np.integer)):
                dtype_conversion['i'] = 'i'
            elif isinstance(val, (float, np.floating)):
                dtype_conversion['i'] = 'f'
            else:
                raise TypeError(f'Cannot replace an integer with {type(val)}')
            dtype = 'i'
            dtype_conversion['f'] = 'f'
        elif isinstance(key, (float, np.floating)):
            if (not isinstance(val, (bool, np.bool_, int, np.integer, float, np.floating))):
                raise TypeError(f'Cannot replace a float with {type(val)}')
            dtype = 'f'
            dtype_conversion['f'] = 'f'
        elif (isinstance(key, str) or (key is None)):
            if ((not isinstance(val, str)) and (val is not None)):
                raise TypeError(f'Cannot replace a str with {type(val)}')
            dtype = 'S'
            dtype_conversion['S'] = 'S'
        elif isinstance(key, np.datetime64):
            if (not isinstance(val, np.datetime64)):
                raise TypeError(f'Cannot replace a datetime64 with {type(val)}')
            dtype = 'M'
            dtype_conversion['M'] = 'M'
        else:
            raise TypeError(f'Unknown replacement type: {type(key)}')
        specific_replacement[dtype].append((key, val))
        if (dtype == 'i'):
            specific_replacement['f'].append((key, val))

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

    def check_to_replace_type(key, col, col_dtype):
        keys = key
        if (not isinstance(keys, tuple)):
            keys = (keys,)
        for key in keys:
            if ((col_dtype == 'b') and (not isinstance(key, (bool, np.bool_)))):
                raise ValueError(f'Column "{col}" is boolean and you are trying to replace {key}, which is of type {type(key)}')
            elif ((col_dtype == 'i') and (not isinstance(key, (bool, np.bool_, int, np.integer)))):
                raise ValueError(f'Column "{col}" is an int and you are trying to replace {key}, which is of type {type(key)}')
            elif ((col_dtype == 'f') and (not isinstance(key, (bool, np.bool_, int, np.integer, float, np.floating)))):
                raise ValueError(f'Column "{col}" is a float and you are trying to replace {key}, which is of type {type(key)}')
            elif ((col_dtype == 'S') and (not isinstance(key, str))):
                raise ValueError(f'Column "{col}" is a str and you are trying to replace {key}, which is of type {type(key)}')
            elif ((col_dtype == 'M') and (not isinstance(key, np.datetime64))):
                raise ValueError(f'Column "{col}" is a datetime64 and you are trying to replace {key}, which is of type {type(key)}')
            elif ((col_dtype == 'm') and (not isinstance(key, np.timedelta64))):
                raise ValueError(f'Column "{col}" is a timedelta64 and you are trying to replace {key}, which is of type {type(key)}')
    col_set = set(self._columns)
    for (key, val) in replace_dict.items():
        if isinstance(val, dict):
            if is_all:
                raise TypeError('`replace_dict` must either be a dictionary of dictionaries or a dictionary of scalars (or tuples) mapped to replacement values. You cannot mix the two.')
            is_one = True
        else:
            if is_one:
                raise TypeError('`replace_dict` must either be a dictionary of dictionaries or a dictionary of scalars (or tuples) mapped to replacement values. You cannot mix the two.')
            is_all = True
        if is_all:
            keys = key
            if (not isinstance(keys, tuple)):
                keys = (keys,)
            for key in keys:
                get_replacement(key, val)
        else:
            if (key not in col_set):
                raise ValueError(f'Column "{key}" not found in DataFrame')
            col_dtype = self._column_info[key].dtype
            for (k, v) in val.items():
                check_to_replace_type(k, key, col_dtype)
                get_replacement_col(col_dtype, k, v, key)
    if is_all:
        used_dtypes = set()
        data_dict = defaultdict(list)
        new_column_info = {}
        (cols, locs, ords) = self._get_all_dtype_info()
        used_dtypes = set(dtype_conversion)
        converted_dtypes = set(dtype_conversion.values())
        cur_dtype_loc = defaultdict(int)
        for (dtype, data) in self._data.items():
            if (dtype not in used_dtypes):
                if (dtype in converted_dtypes):
                    data_dict[dtype].append(data)
                else:
                    data_dict[dtype].append(data.copy('F'))
                for (col, loc, order) in zip(cols[dtype], locs[dtype], ords[dtype]):
                    new_column_info[col] = utils.Column(dtype, loc, order)
                cur_dtype_loc[dtype] = data.shape[1]
        for (dtype, new_dtype) in dtype_conversion.items():
            used_dtypes.add(dtype)
            old_name = utils.convert_dtype_to_func_name(dtype)
            new_name = utils.convert_dtype_to_func_name(new_dtype)
            func_name = f'replace_{old_name}_with_{new_name}'
            dtype_word = utils.convert_kind_to_numpy(dtype)
            new_dtype_word = utils.convert_kind_to_numpy(new_dtype)
            if (new_dtype_word == 'float'):
                dtype_word = 'float'
            elif ((new_dtype_word == 'int') and (dtype_word == 'bool')):
                dtype_word = 'int'
            cur_replacement = specific_replacement[dtype]
            n = len(cur_replacement)
            to_replace = np.empty(n, dtype=dtype_word)
            replacements = np.empty(n, dtype=new_dtype_word)
            for (i, (repl, repl_with)) in enumerate(cur_replacement):
                to_replace[i] = repl
                replacements[i] = repl_with
            func = getattr(_repl, func_name)
            data = self._data[dtype]
            if (dtype in 'mM'):
                data_dict[new_dtype].append(func(data.view('int64'), to_replace.view('int64'), replacements.view('int64')))
            else:
                data_dict[new_dtype].append(func(data, to_replace, replacements))
            loc_add = cur_dtype_loc[new_dtype]
            for (col, loc, order) in zip(cols[dtype], locs[dtype], ords[dtype]):
                new_column_info[col] = utils.Column(new_dtype, (loc + loc_add), order)
            cur_dtype_loc[new_dtype] += data.shape[1]
        new_data = {}
        for (dtype, data) in data_dict.items():
            new_data[dtype] = np.column_stack(data)
        new_columns = self._columns.copy()
    else:
        unused_dtypes = set(self._data)
        used_dtypes = set()
        for (col, dtype) in dtype_conversion.items():
            old_dtype = self._column_info[col].dtype
            unused_dtypes.discard(dtype)
            unused_dtypes.discard(old_dtype)
            used_dtypes.add(dtype)
            used_dtypes.add(old_dtype)
        (cols, locs, ords) = self._get_all_dtype_info()
        new_columns = self._columns.copy()
        new_column_info = {}
        new_data = {}
        for dtype in unused_dtypes:
            new_data[dtype] = self._data[dtype].copy('F')
            for (col, loc, order) in zip(cols[dtype], locs[dtype], ords[dtype]):
                new_column_info[col] = utils.Column(dtype, loc, order)
        used_dtype_ncols = {}
        for dtype in used_dtypes:
            used_dtype_ncols[dtype] = self._data[dtype].shape[1]
        for (col, new_dtype) in dtype_conversion.items():
            used_dtype_ncols[new_dtype] += 1
            old_dtype = self._column_info[col].dtype
            used_dtype_ncols[old_dtype] -= 1
        for (dtype, ncol) in used_dtype_ncols.items():
            nr = len(self)
            dtype_word = utils.convert_kind_to_numpy(dtype)
            new_data[dtype] = np.empty((nr, ncol), dtype=dtype_word)
        cur_dtype_loc = defaultdict(int)
        for dtype in used_dtypes:
            for (col, old_loc, order) in zip(cols[dtype], locs[dtype], ords[dtype]):
                if (col not in specific_replacement):
                    loc = cur_dtype_loc[dtype]
                    new_column_info[col] = utils.Column(dtype, loc, order)
                    new_data[dtype][(:, loc)] = self._data[dtype][(:, old_loc)]
                    cur_dtype_loc[dtype] += 1
                else:
                    (old_dtype, old_loc, order) = self._column_info[col].values
                    new_dtype = dtype_conversion[col]
                    old_name = utils.convert_dtype_to_func_name(old_dtype)
                    new_name = utils.convert_dtype_to_func_name(new_dtype)
                    func_name = f'replace_{old_name}_with_{new_name}'
                    cur_replacement = specific_replacement[col]
                    n = len(cur_replacement)
                    dtype_word = utils.convert_kind_to_numpy(old_dtype)
                    new_dtype_word = utils.convert_kind_to_numpy(new_dtype)
                    if (new_dtype_word == 'float'):
                        dtype_word = 'float'
                    elif ((new_dtype_word == 'int') and (dtype_word == 'bool')):
                        dtype_word = 'int'
                    to_replace = np.empty(n, dtype=dtype_word)
                    replacements = np.empty(n, dtype=new_dtype_word)
                    for (i, (repl, repl_with)) in enumerate(cur_replacement):
                        to_replace[i] = repl
                        replacements[i] = repl_with
                    func = getattr(_repl, func_name)
                    data = self._data[old_dtype][(:, old_loc)][(:, np.newaxis)]
                    loc = cur_dtype_loc[new_dtype]
                    if (old_dtype in 'mM'):
                        data = data.view('int64')
                        to_replace = (to_replace.view('int64'),)
                        replacements = replacements.view('int64')
                    new_data[new_dtype][(:, loc)] = func(data, to_replace, replacements).squeeze()
                    new_column_info[col] = utils.Column(new_dtype, loc, order)
                    cur_dtype_loc[new_dtype] += 1
    return self._construct_from_new(new_data, new_column_info, new_columns)
