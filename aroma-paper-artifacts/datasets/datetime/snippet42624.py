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


def astype(self, dtype: Union[(Dict[(str, str)], str)]) -> 'DataFrame':
    '\n        Changes the data type of one or more columns. Valid data types are\n        int, float, bool, str. Change all the columns as once by passing a string, otherwise\n        use a dictionary of column names mapped to their data type\n\n        Parameters\n        ----------\n        dtype : str or dict mapping column names to data type\n\n        Returns\n        -------\n        New DataFrame with new data types\n\n        '

    def change_each_array(new_loc, new_kind, old_kind, arr, new_arr, cur_srm):
        missing_value_code = utils.get_missing_value_code(new_kind)
        if (new_kind == 'S'):
            if (old_kind == 'b'):
                arr = (arr + 1)
                cur_srm = [False, 'False', 'True']
            elif (old_kind in 'i'):
                (cur_srm, arr) = _va.convert_int_to_str(arr)
            elif (old_kind == 'f'):
                (cur_srm, arr) = _va.convert_float_to_str(arr)
            elif (old_kind in 'mM'):
                (cur_srm, arr) = _va.convert_datetime_str_to_str(arr.astype('str'))
            new_arr[(:, new_loc)] = arr
            new_srm[new_loc] = cur_srm
        else:
            if (new_kind != old_kind):
                nas = utils.isna_array(arr, old_kind)
            if ((new_kind == 'b') and (old_kind != 'b')):
                arr = arr.astype('bool').astype('int8')
            new_arr[(:, new_loc)] = arr
            if (new_kind != old_kind):
                new_arr[(nas, new_loc)] = missing_value_code
    if isinstance(dtype, str):
        new_dtype: str = utils.check_valid_dtype_convert(dtype)
        new_kind: str = utils.convert_numpy_to_kind(new_dtype)
        utils.check_astype_compatible(new_kind, self._data.keys())
        new_column_info: ColInfoT = {}
        new_arr = utils.create_empty_arr(new_kind, self.shape)
        new_data = {new_kind: new_arr}
        new_srm = {}
        col_iter = enumerate(self._col_info_iter(with_order=True, with_arr=True))
        for (i, (col, old_kind, loc, order, arr)) in col_iter:
            new_column_info[col] = utils.Column(new_kind, i, order)
            if (old_kind == 'S'):
                cur_srm = self._str_reverse_map[loc].copy()
            else:
                cur_srm = []
            change_each_array(i, new_kind, old_kind, arr, new_arr, cur_srm)
    elif isinstance(dtype, dict):
        col_kind_convert = {}
        for (col, new_dtype) in dtype.items():
            self._validate_column_name(col)
            new_dtype: str = utils.check_valid_dtype_convert(new_dtype)
            new_kind: str = utils.convert_numpy_to_kind(new_dtype)
            col_kind_convert[col] = new_kind
            old_kind = self._column_info[col].dtype
            utils.check_astype_compatible(new_kind, {old_kind})
        new_column_info: ColInfoT = {}
        cols_per_kind: Dict[(str, int)] = defaultdict(int)
        for (col, old_kind, loc, order) in self._col_info_iter(with_order=True):
            new_kind = col_kind_convert.get(col, old_kind)
            cur_loc = cols_per_kind[new_kind]
            new_column_info[col] = utils.Column(new_kind, cur_loc, order)
            cols_per_kind[new_kind] += 1
        new_data = {}
        for (new_kind, num_cols) in cols_per_kind.items():
            shape = (len(self), num_cols)
            new_data[new_kind] = utils.create_empty_arr(new_kind, shape)
        new_srm = {}
        for (col, old_kind, loc, order, arr) in self._col_info_iter(with_order=True, with_arr=True):
            new_kind = new_column_info[col].dtype
            new_loc = new_column_info[col].loc
            new_arr = new_data[new_kind]
            if (old_kind == 'S'):
                cur_srm = self._str_reverse_map[loc].copy()
            else:
                cur_srm = []
            change_each_array(new_loc, new_kind, old_kind, arr, new_arr, cur_srm)
    else:
        raise TypeError('Argument dtype must be either a string or a dictionary')
    new_columns = self._columns.copy()
    return self._construct_from_new(new_data, new_column_info, new_columns, new_srm)
