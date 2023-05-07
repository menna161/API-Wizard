import dexplo._utils as utils
from dexplo._libs import string_funcs as _sf, date as _date, timedelta as _td
import numpy as np
from numpy import nan, ndarray
from typing import Union, Dict, List, Optional, Tuple, Callable, overload, NoReturn, Set, Iterable, Any, TypeVar, Type, Generator
import datetime


def _month(self, data):
    if (data.size < 6000):
        return _date.month(data.astype('datetime64[M]').astype('int64'))
    else:
        return _date.month2(data.astype('int64'))
