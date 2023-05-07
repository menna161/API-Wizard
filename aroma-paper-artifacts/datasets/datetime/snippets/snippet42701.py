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
