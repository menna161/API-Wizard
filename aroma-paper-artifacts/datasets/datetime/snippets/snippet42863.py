import decimal
from typing import List, Dict, Set, Any, Union, Tuple, Iterable
import numpy as np
from numpy import ndarray
from ._libs import validate_arrays as va


def convert_1d_array(arr: ndarray) -> ndarray:
    arr = try_to_squeeze_array(arr)
    kind: str = arr.dtype.kind
    if (kind in 'ifU'):
        return arr
    elif (kind == 'S'):
        return arr.astype('U')
    elif (kind == 'M'):
        return arr.astype('datetime64[ns]')
    elif (kind == 'm'):
        return arr.astype('timedelta64[ns]')
    elif (kind == 'b'):
        return arr.astype('int8')
    else:
        raise NotImplementedError(f'Data type {kind} unknown')
