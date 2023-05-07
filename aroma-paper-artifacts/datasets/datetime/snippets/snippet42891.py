import decimal
from typing import List, Dict, Set, Any, Union, Tuple, Iterable
import numpy as np
from numpy import ndarray
from ._libs import validate_arrays as va


def get_missing_value_array(kind, n):
    if (kind == 'b'):
        return np.full(n, (- 1), 'int8', 'F')
    elif (kind == 'i'):
        return np.full(n, MIN_INT, 'int64', 'F')
    elif (kind == 'f'):
        return np.full(n, np.nan, 'float64', 'F')
    elif (kind == 'M'):
        return np.full(n, NaT, 'datetime64[ns]', 'F')
    elif (kind == 'M'):
        return np.full(n, NaT, 'timedelta64[ns]', 'F')
    elif (kind == 'S'):
        return np.full(n, 0, 'int32', 'F')
