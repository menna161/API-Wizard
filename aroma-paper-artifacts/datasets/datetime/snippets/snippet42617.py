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


def _setitem_entire_column(self, cs: str, value: Union[(Scalar, ndarray, 'DataFrame')]) -> None:
    "\n        Called when setting an entire column (old or new)\n        df[:, 'col'] = value\n        "
    srm = []
    if utils.is_scalar(value):
        arr: ndarray = np.repeat(value, len(self))
        kind = arr.dtype.kind
    elif isinstance(value, list):
        utils.validate_array_size(value, len(self))
        arr = value
        kind = 'O'
    elif isinstance(value, ndarray):
        utils.validate_array_size(value, len(self))
        arr = utils.try_to_squeeze_array(value)
        kind = arr.dtype.kind
    elif isinstance(value, DataFrame):
        if (value.shape[0] != self.shape[0]):
            raise ValueError(f'The DataFrame on the left has {self.shape[0]} rows. The DataFrame on the right has {self.shape[0]} rows. They must be equal')
        if (value.shape[1] != 1):
            raise ValueError(f'You are setting exactly one column. The DataFrame you are trying to set this with has {value.shape[1]} columns. They must be equal')
        col = value.columns[0]
        (kind, loc, _) = value._column_info[col].values
        arr = value._data[kind][(:, loc)]
        if (kind == 'S'):
            srm = value._str_reverse_map[loc]
        self._full_columm_add(cs, kind, arr, srm)
    else:
        raise TypeError('Must use a scalar, a list, an array, or a DataFrame when setting new values')
    if (kind == 'O'):
        (arr, kind, srm) = _va.convert_object_array(arr, cs)
    elif (kind == 'b'):
        arr = arr.astype('int8')
    elif (kind in 'SU'):
        arr = arr.astype('U')
        (arr, kind, srm) = _va.convert_str_to_cat(arr)
    elif (kind == 'M'):
        arr = arr.astype('datetime64[ns]')
    elif (kind == 'm'):
        arr = arr.astype('timedelta64[ns]')
    self._full_columm_add(cs, kind, arr, srm)
