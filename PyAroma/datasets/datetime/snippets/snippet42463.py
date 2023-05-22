import dexplo._utils as utils
from dexplo._libs import string_funcs as _sf, date as _date, timedelta as _td
import numpy as np
from numpy import nan, ndarray
from typing import Union, Dict, List, Optional, Tuple, Callable, overload, NoReturn, Set, Iterable, Any, TypeVar, Type, Generator
import datetime


def _is_leap_year(self, data):
    if (data.size < 500):
        years = (data.astype('datetime64[Y]').astype('float64') + 1970)
        years[np.isnat(data)] = nan
        return np.where(((years % 4) == 0), np.where(((years % 100) == 0), np.where(((years % 400) == 0), True, False), True), False)
    else:
        return _date.is_leap_year(data.astype('int64'))
