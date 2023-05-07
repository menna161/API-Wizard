import dexplo._utils as utils
from dexplo._libs import string_funcs as _sf, date as _date, timedelta as _td
import numpy as np
from numpy import nan, ndarray
from typing import Union, Dict, List, Optional, Tuple, Callable, overload, NoReturn, Set, Iterable, Any, TypeVar, Type, Generator
import datetime


def _day(self, data):
    if (data.size < 5000):
        days = ((data.astype('datetime64[D]') - data.astype('datetime64[M]')) + 1).astype('float64')
        days[np.isnat(data)] = nan
    else:
        return _date.day(data.astype('int64'))
    return days
