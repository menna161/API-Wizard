import dexplo._utils as utils
from dexplo._libs import string_funcs as _sf, date as _date, timedelta as _td
import numpy as np
from numpy import nan, ndarray
from typing import Union, Dict, List, Optional, Tuple, Callable, overload, NoReturn, Set, Iterable, Any, TypeVar, Type, Generator
import datetime


def _day_of_year(self, data):
    if (data.size < 2500):
        doy = ((data.astype('datetime64[D]') - data.astype('datetime64[Y]')) + 1).astype('float64')
        doy[np.isnat(data)] = nan
        return doy
    else:
        return _date.day_of_year(data.astype('int64'))
