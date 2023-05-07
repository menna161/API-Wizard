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


def drop(self, rows: Union[(int, List[int], ndarray, None)]=None, columns: Union[(str, int, List[IntStr], ndarray, None)]=None):
    if (rows is None):
        return self._drop_just_cols(columns)
    if (columns is None):
        return self._drop_just_rows(rows)
    if isinstance(columns, (int, str, np.integer)):
        columns = [columns]
    elif isinstance(columns, ndarray):
        columns = utils.try_to_squeeze_array(columns)
    elif (not isinstance(columns, list)):
        raise TypeError('Rows must either be an int, list/array of ints or None')
    if isinstance(rows, int):
        rows = [rows]
    elif isinstance(rows, ndarray):
        rows = utils.try_to_squeeze_array(rows)
    elif (not isinstance(rows, list)):
        raise TypeError('Rows must either be an int, list/array of ints or None')
    new_rows: List[int] = []
    for row in rows:
        if (not isinstance(row, int)):
            raise TypeError('All the row values in your list must be integers')
        if ((row < (- len(self))) or (row >= len(self))):
            raise IndexError(f'Integer location {row} for the rows is out of range')
        if (row < 0):
            new_rows.append((len(self) + row))
        else:
            new_rows.append(row)
    column_strings: List[str] = []
    for col in columns:
        if isinstance(col, str):
            column_strings.append(col)
        elif isinstance(col, (int, np.integer)):
            column_strings.append(self._columns[col])
    self._validate_column_name_list(column_strings)
    column_set: Set[str] = set(column_strings)
    new_rows = np.isin(np.arange(len(self)), new_rows, invert=True)
    new_columns = [col for col in self._columns if (col not in column_set)]
    new_column_info: ColInfoT = {}
    data_dict: Dict[(str, List[int])] = defaultdict(list)
    for (i, col) in enumerate(new_columns):
        (dtype, loc) = self._get_col_dtype_loc(col)
        cur_loc = len(data_dict[dtype])
        new_column_info[col] = utils.Column(dtype, cur_loc, i)
        data_dict[dtype].append(loc)
    new_data = {}
    for (dtype, locs) in data_dict.items():
        new_data[dtype] = self._data[dtype][np.ix_(new_rows, locs)]
    return self._construct_from_new(new_data, new_column_info, np.asarray(new_columns, dtype='O'))
