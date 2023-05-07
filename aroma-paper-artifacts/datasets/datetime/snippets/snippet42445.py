import dexplo._utils as utils
from dexplo._libs import string_funcs as _sf, date as _date, timedelta as _td
import numpy as np
from numpy import nan, ndarray
from typing import Union, Dict, List, Optional, Tuple, Callable, overload, NoReturn, Set, Iterable, Any, TypeVar, Type, Generator
import datetime


def _generic_concat(self, name, column, keep, **kwargs):
    if (not isinstance(keep, (bool, np.bool_))):
        raise TypeError('`keep` must be a boolean')
    if (column is None):
        columns = []
        locs = []
        for (col, dtype, loc) in self._df._col_info_iter():
            if (dtype == self._dtype_acc):
                columns.append(col)
                locs.append(loc)
    else:
        (columns, locs) = self._validate_columns(column)
    data = self._df._data[self._dtype_acc]
    arrs = []
    all_cols = []
    for loc in locs:
        (arr, new_columns) = getattr(_sf, name)(data[(:, loc)], **kwargs)
        arrs.append(arr)
        all_cols.append(new_columns)
    dtype_new = arrs[0].dtype.kind
    if (len(arrs) == 1):
        final_arr = arrs[0]
        final_cols = all_cols[0]
    else:
        final_arr = np.column_stack(arrs)
        all_cols_new = []
        for (cols, orig_name) in zip(all_cols, columns):
            all_cols_new.append(((cols + '_') + orig_name))
        final_cols = np.concatenate(all_cols_new)
    new_column_info = {}
    new_data = {}
    add_loc = 0
    add_order = 0
    if keep:
        df = self._df.drop(columns=columns)
        if (dtype_new in df._data):
            add_loc = df._data[dtype_new].shape[1]
        add_order = df.shape[1]
        for (dtype, arr) in df._data.items():
            if (dtype == dtype_new):
                new_data[dtype_new] = np.column_stack((arr, final_arr))
            else:
                new_data[dtype] = arr.copy('F')
        if (dtype_new not in df._data):
            new_data[dtype_new] = final_arr
        new_column_info = df._copy_column_info()
        new_columns = np.concatenate((df._columns, final_cols))
    else:
        new_data = {dtype_new: final_arr}
        new_columns = final_cols
    for (i, col) in enumerate(final_cols):
        new_column_info[col] = utils.Column(dtype_new, (i + add_loc), (i + add_order))
    return self._df._construct_from_new(new_data, new_column_info, new_columns)
