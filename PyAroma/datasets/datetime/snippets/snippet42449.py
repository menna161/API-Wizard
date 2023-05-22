import dexplo._utils as utils
from dexplo._libs import string_funcs as _sf, date as _date, timedelta as _td
import numpy as np
from numpy import nan, ndarray
from typing import Union, Dict, List, Optional, Tuple, Callable, overload, NoReturn, Set, Iterable, Any, TypeVar, Type, Generator
import datetime


def _ceil(self, data, freq):
    if (freq == 'ns'):
        return data
    if (freq == 'Y'):
        if (data.size < 5000):
            years = data.astype('datetime64[Y]')
            diff = (years - data).astype('int64')
            years[(diff != 0)] += 1
            return years.astype('datetime64[ns]')
    return getattr(_date, ('ceil_' + freq))(data.astype('float64'))
