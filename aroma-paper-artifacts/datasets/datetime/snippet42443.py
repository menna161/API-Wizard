import dexplo._utils as utils
from dexplo._libs import string_funcs as _sf, date as _date, timedelta as _td
import numpy as np
from numpy import nan, ndarray
from typing import Union, Dict, List, Optional, Tuple, Callable, overload, NoReturn, Set, Iterable, Any, TypeVar, Type, Generator
import datetime


def _create_df_multiple_dtypes(self, arr_new, columns, column_locs, columns_other, locs_other):
    new_data = {}
    dtype_new = arr_new.dtype.kind
    try:
        add_loc = self._df._data[dtype_new].shape[1]
    except KeyError:
        add_loc = 0
    for (dtype, arr) in self._df._data.items():
        if (dtype == self._dtype_acc):
            new_data[self._dtype_acc] = arr[(:, locs_other)]
        elif (dtype == dtype_new):
            new_data[dtype_new] = np.asfortranarray(np.column_stack((arr, arr_new)))
        else:
            new_data[dtype] = arr.copy('F')
    if (dtype_new not in new_data):
        new_data[dtype_new] = arr_new
    new_column_info = {}
    for (col, old_dtype, loc, order) in self._df._col_info_iter(with_order=True):
        if (old_dtype != self._dtype_acc):
            new_column_info[col] = utils.Column(old_dtype, loc, order)
    for (i, (col, loc)) in enumerate(zip(columns, column_locs)):
        order = self._df._column_info[col].order
        new_column_info[col] = utils.Column(dtype_new, (add_loc + i), order)
    for (i, col) in enumerate(columns_other):
        order = self._df._column_info[col].order
        new_column_info[col] = utils.Column(self._dtype_acc, i, order)
    return self._df._construct_from_new(new_data, new_column_info, self._df._columns.copy())
