import dexplo._utils as utils
from dexplo._libs import string_funcs as _sf, date as _date, timedelta as _td
import numpy as np
from numpy import nan, ndarray
from typing import Union, Dict, List, Optional, Tuple, Callable, overload, NoReturn, Set, Iterable, Any, TypeVar, Type, Generator
import datetime


def _year(self, data):
    if (data.size < 5000):
        years = (data.astype('datetime64[Y]').astype('float64') + 1970)
        years[np.isnat(data)] = nan
        return years
    else:
        return _date.year(data.astype('int64'))
