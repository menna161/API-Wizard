import decimal
from typing import List, Dict, Set, Any, Union, Tuple, Iterable
import numpy as np
from numpy import ndarray
from ._libs import validate_arrays as va


def convert_numpy_to_kind(dtype: str) -> str:
    try:
        return _NP_KIND[dtype]
    except KeyError:
        dt = dtype.split('[')[0]
        if (dt == 'datetime64'):
            return 'M'
        elif (dt == 'timedelta64'):
            return 'm'
