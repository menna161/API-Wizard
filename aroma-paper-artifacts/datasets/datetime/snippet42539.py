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


def _build_repr(self) -> Tuple[(List[List[str]], List[int], List[int], List[int])]:
    columns: List[str] = self.columns
    num_rows: int = len(self)
    max_cols = options.options_dict['max_cols']
    max_rows = options.options_dict['max_rows']
    max_colwidth = options.options_dict['max_colwidth']
    if options._head_method:
        max_rows = num_rows
    if (len(columns) > max_cols):
        col_num: int = (max_cols // 2)
        columns = ((columns[:col_num] + ['...']) + columns[(- col_num):])
    if (num_rows > max_rows):
        if options.options_dict['show_tail']:
            first: List[int] = list(range((max_rows // 2)))
            last: List[int] = list(range((num_rows - (max_rows // 2)), num_rows))
            idx: List[int] = (first + last)
        else:
            idx = list(range(max_rows))
    else:
        idx = list(range(num_rows))
    data_list: List[List[str]] = [([''] + [str(i) for i in idx])]
    long_len: List[int] = [len(data_list[0][(- 1)])]
    decimal_len: List[int] = [0]
    data: List
    cur_len: int
    dec_len: List
    whole_len: List
    dec_len_arr: ndarray
    whole_len_arr: ndarray
    for column in columns:
        if (column != '...'):
            vals = self._get_column_values(column)[idx]
            dtype = self._column_info[column].dtype
            if (dtype == 'M'):
                unit = utils.get_datetime_str(vals)
                vals = vals.astype(f'datetime64[{unit}]')
                data = ([column] + [(str(val).replace('T', ' ') if (not np.isnat(val)) else str(val)) for val in vals])
            elif (dtype == 'm'):
                unit = utils.get_timedelta_str(vals)
                vals = vals.astype(f'timedelta64[{unit}]')
                data = ([column] + [(str(val).replace('T', ' ') if (not np.isnat(val)) else str(val)) for val in vals])
            elif (dtype == 'S'):
                loc = self._column_info[column].loc
                rev_map = self._str_reverse_map[loc]
                data = ([column] + [('NaN' if (val == 0) else rev_map[val]) for val in vals])
            elif (dtype == 'i'):
                data = ([column] + [('NaN' if (val == MIN_INT) else val) for val in vals])
            elif (dtype == 'b'):
                bool_dict = {(- 1): 'NaN', 0: 'False', 1: 'True'}
                data = ([column] + [bool_dict[val] for val in vals])
            elif (dtype == 'f'):
                data = ([column] + [('NaN' if np.isnan(val) else val) for val in vals])
        else:
            data = (['...'] * (len(idx) + 1))
            long_len.append(3)
            decimal_len.append(0)
            data_list.append(data)
            continue
        if (len(self) == 0):
            data_list.append(data)
            long_len.append(len(column))
            decimal_len.append(0)
            continue
        if (self._column_info[column].dtype == 'S'):
            cur_len = max([len(str(x)) for x in data])
            cur_len = min(cur_len, max_colwidth)
            long_len.append(cur_len)
            decimal_len.append(0)
        elif (self._column_info[column].dtype == 'f'):
            dec_len = [utils.get_decimal_len(x) for x in data[1:]]
            whole_len = [utils.get_whole_len(x) for x in data[1:]]
            dec_len_arr = np.array(dec_len).clip(0, 6)
            whole_len_arr = np.array(whole_len)
            lengths = [len(column), ((dec_len_arr.max() + whole_len_arr.max()) + 1)]
            max_decimal = dec_len_arr.max()
            long_len.append(max(lengths))
            decimal_len.append(min(max_decimal, 6))
        elif (self._column_info[column].dtype == 'i'):
            lengths = ([len(column)] + [len(str(x)) for x in data[1:]])
            long_len.append(max(lengths))
            decimal_len.append(0)
        elif (self._column_info[column].dtype == 'b'):
            long_len.append(max(len(column), 5))
            decimal_len.append(0)
        elif (self._column_info[column].dtype in 'Mm'):
            long_len.append(max(len(column), len(data[1])))
            decimal_len.append(0)
        data_list.append(data)
    return (data_list, long_len, decimal_len, idx)
