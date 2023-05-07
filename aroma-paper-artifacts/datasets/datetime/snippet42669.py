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


def _replace_nans(self, dtype: str, col_arr: ndarray, asc: bool, hasnans: ndarray, return_na_arr: bool=False):
    if (dtype == 'S'):
        if (hasnans or (hasnans is None)):
            if asc:
                nan_value = chr((10 ** 6))
            else:
                nan_value = ''
            if (col_arr.ndim == 1):
                na_arr: ndarray = _math.isna_str_1d(col_arr)
                arr_final: ndarray = np.where(na_arr, nan_value, col_arr)
            else:
                hasnans = np.array(([True] * col_arr.shape[1]))
                na_arr = _math.isna_str(col_arr, hasnans)
                arr_final = np.where(na_arr, nan_value, col_arr)
    elif (dtype == 'f'):
        if (hasnans or (hasnans is None)):
            if asc:
                nan_value = np.inf
            else:
                nan_value = (- np.inf)
            na_arr = np.isnan(col_arr)
            arr_final = np.where(na_arr, nan_value, col_arr)
    elif (dtype in 'mM'):
        if (hasnans or (hasnans is None)):
            if asc:
                if (dtype == 'M'):
                    nan_value = np.datetime64(np.iinfo('int64').max, 'ns')
                else:
                    nan_value = np.timedelta64(np.iinfo('int64').max, 'ns')
            elif (dtype == 'M'):
                nan_value = np.datetime64(np.iinfo('int64').min, 'ns')
            else:
                nan_value = np.timedelta64(np.iinfo('int64').min, 'ns')
            na_arr = np.isnat(col_arr)
            arr_final = np.where(na_arr, nan_value, col_arr)
    else:
        return col_arr
    if return_na_arr:
        return (arr_final, na_arr)
    else:
        return arr_final
