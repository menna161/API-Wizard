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


def sample(self, n: Optional[int]=None, frac: Optional[float]=None, replace: bool=False, weights: Union[(List, ndarray, None)]=None, random_state: Optional[Any]=None, axis: str='rows') -> 'DataFrame':
    axis_num = utils.convert_axis_string(axis)
    if (axis_num == 1):
        raise NotImplementedError('No sampling columns yet')
    if (not isinstance(replace, (bool, np.bool_))):
        raise TypeError('`replace` must be either True or False')
    if (weights is not None):
        if ((axis_num == 0) and (len(weights) != len(self))):
            raise ValueError('`weights` must have the same number of elements as the number of rows in the DataFrame ')
        if ((axis_num == 1) and (len(weights) != len(self._columns))):
            raise ValueError('`weights` must have the same number of elements as the number of columns in the DataFrame ')
        weights = np.asarray(weights)
        weights = utils.try_to_squeeze_array(weights)
        if (weights.dtype.kind not in ('i', 'f')):
            raise TypeError('All values in `weights` must be numeric')
        weight_sum = weights.sum()
        if np.isnan(weight_sum):
            weights[np.isnan(weights)] = 0
            weight_sum = weights.sum()
        if (weight_sum <= 0):
            raise ValueError('The sum of the weights is <= 0. ')
        weights = (weights / weight_sum)
    if (random_state is not None):
        if isinstance(random_state, (int, np.integer)):
            random_state = np.random.RandomState(random_state)
        elif (not isinstance(random_state, np.random.RandomState)):
            raise TypeError('`random_state` must either be ')
    if (axis_num == 0):
        axis_len = len(self)
    else:
        axis_len = len(self._columns)
    if (n is not None):
        if (not isinstance(n, (int, np.integer))):
            raise TypeError('`n` must be either an integer or None')
        if (n < 1):
            raise ValueError('`n` must greater than 0')
        if (frac is not None):
            raise ValueError('You cannot specify both `n` and `frac`. Choose one or the other.')
    else:
        if (frac is None):
            raise ValueError('`n` and `frac` cannot both be None. One and only one must be set')
        if ((not isinstance(frac, (int, float, np.number))) or (frac <= 0)):
            raise ValueError('`frac` must be a number greater than 0')
        n = ceil((frac * axis_len))
    if (random_state is None):
        if ((weights is None) and replace):
            new_idx = np.random.randint(0, axis_len, n)
        else:
            new_idx = np.random.choice(np.arange(axis_len), n, replace, weights)
    else:
        new_idx = random_state.choice(np.arange(axis_len), n, replace, weights)
    if (axis_num == 0):
        new_columns = self._columns.copy()
        new_column_info = self._copy_column_info()
        new_data = {}
        for (dtype, arr) in self._data.items():
            new_data[dtype] = arr[new_idx]
        return self._construct_from_new(new_data, new_column_info, new_columns)
    else:
        column_ints: Dict[(str, int)] = defaultdict(int)
        data_dict: DictListArr = defaultdict(list)
        new_columns = []
        new_column_info = {}
        for (i, num) in enumerate(new_idx):
            col = self._columns[num]
            (dtype, loc) = self._get_col_dtype_loc(col)
            cur_col_num = column_ints[col]
            if (cur_col_num == 0):
                col_new = col
            else:
                col_new = (col + str(cur_col_num))
            column_ints[col] += 1
            new_column_info[col_new] = utils.Column(dtype, cur_col_num, i)
            data_dict[dtype].append(self._data[dtype][(:, [loc])])
            new_columns.append(col_new)
        new_data = utils.concat_data_arrays(data_dict)
        return self._construct_from_new(new_data, new_column_info, np.asarray(new_columns, dtype='O'))
