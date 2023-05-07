import decimal
from typing import List, Dict, Set, Any, Union, Tuple, Iterable
import numpy as np
from numpy import ndarray
from ._libs import validate_arrays as va


def check_valid_dtype_convert(dtype: str) -> str:
    if (dtype not in _DTYPES):
        raise ValueError(f'{dtype} is not a valid type. Must be one of int, float, bool, str, datetime64[X], timedelta64[X], where `X` is one of ns, us, ms, s, m, h, D, W, M, Y')
    return _DTYPES[dtype]
