import dexplo._utils as utils
from dexplo._libs import string_funcs as _sf, date as _date, timedelta as _td
import numpy as np
from numpy import nan, ndarray
from typing import Union, Dict, List, Optional, Tuple, Callable, overload, NoReturn, Set, Iterable, Any, TypeVar, Type, Generator
import datetime


def _quarter(self, data):
    if (data.size < 5000):
        t = (((data.astype('datetime64[M]').astype('float64') % 12) // 3) + 1)
        t[np.isnat(data)] = nan
        return t
    else:
        return _date.quarter(data.astype('int64'))
