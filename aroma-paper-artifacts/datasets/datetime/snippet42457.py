import dexplo._utils as utils
from dexplo._libs import string_funcs as _sf, date as _date, timedelta as _td
import numpy as np
from numpy import nan, ndarray
from typing import Union, Dict, List, Optional, Tuple, Callable, overload, NoReturn, Set, Iterable, Any, TypeVar, Type, Generator
import datetime


def _days_in_month(self, data):
    if (data.size < 5000):
        month = data.astype('datetime64[M]')
        next_month = (month + 1).astype('datetime64[D]')
        dim = (next_month - month).astype('float64')
        dim[np.isnat(data)] = nan
        return dim
    else:
        return _date.days_in_month(data.astype('int64'))
