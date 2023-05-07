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


def where(self, cond: Union[(ndarray, 'DataFrame')], x: Union[(Scalar, ndarray, 'DataFrame', None)]=None, y: Union[(Scalar, ndarray, 'DataFrame', None)]=None) -> 'DataFrame':
    if isinstance(cond, DataFrame):
        cond = cond.values
    if isinstance(cond, ndarray):
        if (cond.ndim == 1):
            cond = cond[(:, np.newaxis)]
        if (cond.dtype.kind != 'b'):
            raise TypeError('The `cond` numpy array must be boolean')
        if (cond.shape[0] != self.shape[0]):
            raise ValueError(f'`cond` array must have the same number of rows as calling DataFrame. {cond.shape[0]} != {self.shape[0]}')
        if ((cond.shape[1] != self.shape[1]) and (cond.shape[1] != 1)):
            raise ValueError('`cond` must have either a single column or have the same number of columns as the calling DataFrame')
    else:
        raise TypeError('`cond` must be either a DataFrame or a NumPy array')
    if (isinstance(x, ndarray) and (x.ndim == 1)):
        x = x[(:, np.newaxis)]
    if (isinstance(y, ndarray) and (y.ndim == 1)):
        y = y[(:, np.newaxis)]
    if isinstance(x, DataFrame):
        x = x.values
    if isinstance(y, DataFrame):
        y = y.values
    for (var, name) in zip([x, y], ['x', 'y']):
        if isinstance(var, ndarray):
            if (var.shape[0] != self.shape[0]):
                raise ValueError(f'`{name} must have the same number of rows as the calling DataFrame')
            if ((var.shape[1] != self.shape[1]) and (var.shape[1] != 1)):
                raise ValueError(f'`{name}` must have either a single column or have the same number of columns of the calling DataFrame')

    def get_arr(arr: ndarray) -> ndarray:
        if (arr.shape[1] == 1):
            return arr
        else:
            return arr[(:, dtype_order[dtype])]

    def get_curr_var(var: Optional[ndarray], dtype: str, name: str) -> Optional[ndarray]:
        if (var is None):
            return (None if (dtype == 'S') else nan)
        types: Any
        if (dtype == 'S'):
            good_dtypes = ['S', 'U']
            types = str
        elif (dtype in 'if'):
            good_dtypes = ['i', 'f']
            types = (int, float, np.number)
        elif (dtype == 'b'):
            good_dtypes = ['b']
            types = (bool, np.bool_)
        elif (dtype == 'M'):
            good_dtypes = ['M']
            types = np.datetime64
        elif (dtype == 'm'):
            good_dtypes = ['m']
            types = np.timedelta64
        if isinstance(var, ndarray):
            var_curr = get_arr(var)
            if (var_curr.dtype.kind not in good_dtypes):
                raise TypeError(f'The array you passed to `{name}` must have compatible dtypes to the same columns in the calling DataFrame')
        elif (not isinstance(var, types)):
            raise TypeError(f'The values you are using to set with `{name}` do not have compatible types with one of the columns')
        else:
            var_curr = var
        return var_curr

    def check_x_y_types(x: Union[(Scalar, ndarray, 'DataFrame', None)], y: Union[(Scalar, ndarray, 'DataFrame', None)]) -> Tuple[(ndarray, ndarray)]:
        if isinstance(x, ndarray):
            x = get_arr(x)
        if isinstance(y, ndarray):
            y = get_arr(y)
        if (isinstance(x, ndarray) and isinstance(y, ndarray)):
            if ((x.dtype.kind in 'if') and (y.dtype.kind not in 'if')):
                raise TypeError('`x` and `y` arrays have incompatible dtypes. `x` is numeric and `y` is not')
            elif (x.dtype.kind != y.dtype.kind):
                raise TypeError('`x` and `y` dtypes are not compatible')
        elif (isinstance(x, ndarray) and utils.is_scalar(y)):
            if ((x.dtype.kind in 'if') and (not isinstance(y, (int, float, np.number)))):
                raise TypeError('`x` and `y` arrays have incompatible dtypes. `x` is numeric and `y` is not')
            elif ((x.dtype.kind == 'S') and (not isinstance(y, str))):
                raise TypeError('`x` and `y` arrays have incompatible dtypes. `x` is str and `y` is not')
            elif ((x.dtype.kind == 'b') and (not isinstance(y, (bool, np.bool_)))):
                raise TypeError('`x` and `y` arrays have incompatible dtypes. `x` is bool and `y` is not')
        elif (utils.is_scalar(x) and isinstance(y, ndarray)):
            if ((y.dtype.kind in 'if') and (not isinstance(x, (int, float, np.number)))):
                raise TypeError('`x` and `y` arrays have incompatible dtypes. `y` is numeric and `x` is not')
            elif ((y.dtype.kind == 'S') and (not isinstance(x, str))):
                raise TypeError('`x` and `y` arrays have incompatible dtypes. `y` is str and `x` is not')
            elif ((y.dtype.kind == 'b') and (not isinstance(x, (bool, np.bool_)))):
                raise TypeError('`x` and `y` arrays have incompatible dtypes. `y` is bool and `x` is not')
        elif (utils.is_scalar(x) and utils.is_scalar(y)):
            if (isinstance(x, (int, float, np.number)) and (not isinstance(y, (int, float, np.number)))):
                raise TypeError('`x` and `y` arrays have incompatible dtypes. `x` is numeric and `y` is not')
            elif (isinstance(x, str) and (not isinstance(y, str))):
                raise TypeError('`x` and `y` arrays have incompatible dtypes. `x` is str and `y` is not')
            elif (isinstance(x, (bool, np.bool_)) and (not isinstance(y, (bool, np.bool_)))):
                raise TypeError('`x` and `y` arrays have incompatible dtypes. `y` is bool and `x` is not')
        else:
            raise TypeError('`x` and `y` must be a scalar, array, DataFrame, or None')
        return (x, y)
    (dtype_col, dtype_loc, dtype_order) = self._get_all_dtype_info()
    data_dict: DictListArr = defaultdict(list)
    new_column_info = {}
    for (dtype, arr) in self._data.items():
        if (cond.shape[1] != 1):
            cond_dtype = cond[(:, dtype_order[dtype])]
        elif (arr.shape[1] != 1):
            cond_dtype = cond[(:, ([0] * arr.shape[1]))]
        else:
            cond_dtype = cond
        if (x is None):
            x_curr = arr[(:, dtype_loc[dtype])]
            y_curr = get_curr_var(y, dtype, 'y')
        elif (y is None):
            x_curr = get_curr_var(x, dtype, 'x')
            y_curr = get_curr_var(y, dtype, 'y')
        else:
            (x_curr, y_curr) = check_x_y_types(x, y)
        arr_new = np.where(cond_dtype, x_curr, y_curr)
        if (arr_new.dtype.kind == 'U'):
            arr_new = arr_new.astype('O')
        new_dtype = arr_new.dtype.kind
        cur_loc = utils.get_num_cols(data_dict.get(new_dtype, []))
        data_dict[new_dtype].append(arr_new)
        for (col, pos, order) in zip(dtype_col[dtype], dtype_loc[dtype], dtype_order[dtype]):
            new_column_info[col] = utils.Column(new_dtype, (pos + cur_loc), order)
    new_columns = self._columns.copy()
    new_data = utils.concat_data_arrays(data_dict)
    return self._construct_from_new(new_data, new_column_info, new_columns)
