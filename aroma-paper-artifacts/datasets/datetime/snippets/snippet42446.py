import dexplo._utils as utils
from dexplo._libs import string_funcs as _sf, date as _date, timedelta as _td
import numpy as np
from numpy import nan, ndarray
from typing import Union, Dict, List, Optional, Tuple, Callable, overload, NoReturn, Set, Iterable, Any, TypeVar, Type, Generator
import datetime


def _generic(self, name, column, keep, multiple, **kwargs):
    if (not isinstance(keep, (bool, np.bool_))):
        raise TypeError('`keep` must be a boolean')
    if keep:
        (columns, locs, other_columns, other_locs) = self._validate_columns_others(column)
    else:
        (columns, locs) = self._validate_columns(column)
    data = self._df._data[self._dtype_acc]
    if (len(locs) == 1):
        arr = getattr(self, name)(data[(:, locs)], **kwargs)
    else:
        arr = getattr(self, name)(data[(:, locs)], **kwargs)
    if keep:
        if multiple:
            return self._create_df_multiple_dtypes(arr, columns, locs, other_columns, other_locs)
        else:
            data = data.copy()
            for (i, loc) in enumerate(locs):
                data[(:, loc)] = arr[(:, i)]
            return self._create_df_all(data, self._dtype_acc)
    else:
        return self._create_df(arr, arr.dtype.kind, columns)
