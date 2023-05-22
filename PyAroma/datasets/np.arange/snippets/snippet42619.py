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


def _setitem_multiple_multiple(self, rows: Union[(List[int], ndarray)], cols: List[str], value: Any) -> None:
    cur_kinds = [self._column_info[col].dtype for col in cols]
    (nrows_to_set, ncols_to_set) = self._setitem_nrows_ncols_to_set(rows, cols)
    arrs: List[ndarray] = []
    kinds = []
    srms = []
    if isinstance(value, list):
        value = utils.convert_lists_vertical(value)
        (arrs, kinds, srms) = utils.convert_to_arrays(value, ncols_to_set, cur_kinds)
    elif isinstance(value, ndarray):
        (arrs, kinds, srms) = utils.convert_to_arrays(value, ncols_to_set, cur_kinds)
    elif isinstance(value, DataFrame):
        for col in value._columns:
            srm = []
            (kind, loc, _) = value._column_info[col].values
            arrs.append(value._data[kind][(:, loc)])
            kinds.append(kind)
            if (kind == 'S'):
                srm = value._str_reverse_map[loc]
            srms.append(srm)
    else:
        raise TypeError('Must use a scalar, a list, an array, or a DataFrame when setting new values')
    utils.setitem_validate_shape(nrows_to_set, ncols_to_set, arrs)
    utils.setitem_validate_col_types(cur_kinds, kinds, cols)
    for (col, arr, k1, k2, cur_srm) in zip(cols, arrs, cur_kinds, kinds, srms):
        if ((k1 == 'i') and (k2 == 'f')):
            dtype_internal: str = utils.convert_kind_to_numpy(k2)
            self._astype_internal(col, dtype_internal)
        (dtype, loc) = self._get_col_dtype_loc(col)
        if (dtype == 'S'):
            old_srm = self._str_reverse_map[loc]
            old_codes = self._data[dtype][(:, loc)]
            str_map = {False: 0}
            new_srm = [False]
            new_codes = np.empty(len(old_codes), 'uint32', 'F')
            if isinstance(rows, slice):
                rows = np.arange(len(self))[rows]
            j = 0
            if (isinstance(rows, ndarray) and (rows.dtype.kind == 'b')):
                for (i, code) in enumerate(old_codes):
                    if rows[i]:
                        cur_str = cur_srm[arr[j]]
                        j += 1
                    else:
                        cur_str = old_srm[code]
                    n_before = len(str_map)
                    new_codes[i] = str_map.setdefault(cur_str, len(str_map))
                    n_after = len(str_map)
                    if (n_after > n_before):
                        new_srm.append(cur_str)
            else:
                for (i, code) in enumerate(old_codes):
                    if ((j < len(rows)) and (rows[j] == i)):
                        cur_str = cur_srm[arr[j]]
                        j += 1
                    else:
                        cur_str = old_srm[code]
                    n_before = len(str_map)
                    new_codes[i] = str_map.setdefault(cur_str, len(str_map))
                    n_after = len(str_map)
                    if (n_after > n_before):
                        new_srm.append(cur_str)
            self._str_reverse_map[loc] = new_srm
            self._data[dtype][(:, loc)] = new_codes
        else:
            self._data[dtype][(rows, loc)] = arr
