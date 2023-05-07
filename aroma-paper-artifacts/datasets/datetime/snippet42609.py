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


def _astype_internal(self, column: str, numpy_dtype: str) -> None:
    '\n        Changes one column dtype in-place\n        '
    new_kind: str = utils.convert_numpy_to_kind(numpy_dtype)
    (dtype, loc, order) = self._get_col_dtype_loc_order(column)
    srm = []
    if (dtype == new_kind):
        return None
    col_data: ndarray = self._data[dtype][(:, loc)]
    nulls = utils.isna_array(col_data, dtype)
    if (numpy_dtype == 'S'):
        col_data = col_data.astype('U')
        (col_data, _, srm) = _va.convert_str_to_cat(col_data)
        col_data[nulls] = 0
    elif (numpy_dtype == 'b'):
        col_data = col_data.astype('bool').astype('int8')
        col_data[nulls] = (- 1)
    elif (numpy_dtype == 'i'):
        col_data = col_data.astype('int64')
        col_data[nulls] = MIN_INT
    elif (numpy_dtype == 'f'):
        col_data = col_data.astype('int64')
        col_data[nulls] = np.nan
    elif (col_data.dtype.kind == 'M'):
        col_data = col_data.astype('datetime64[ns]')
        col_data[nulls] = NaT
    elif (col_data.dtype.kind == 'm'):
        col_data = col_data.astype('timedelta64[ns]')
        col_data[nulls] = NaT
    self._remove_column(column)
    self._write_new_column_data(column, new_kind, col_data, srm, order)
