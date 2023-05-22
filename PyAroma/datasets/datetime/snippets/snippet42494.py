import dexplo._utils as utils
from dexplo._libs import string_funcs as _sf, date as _date, timedelta as _td
import numpy as np
from numpy import nan, ndarray
from typing import Union, Dict, List, Optional, Tuple, Callable, overload, NoReturn, Set, Iterable, Any, TypeVar, Type, Generator
import datetime


def to_pytime(self, column=None):
    (columns, locs) = self._validate_columns(column)
    data = self._df._data['M'][(:, locs)]
    return _date.to_pytime(data.astype('float64'))
