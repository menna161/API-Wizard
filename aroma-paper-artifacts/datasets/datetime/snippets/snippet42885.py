import decimal
from typing import List, Dict, Set, Any, Union, Tuple, Iterable
import numpy as np
from numpy import ndarray
from ._libs import validate_arrays as va


def try_to_convert_dtype(dtype: str) -> List[str]:
    try:
        return _KIND_LIST[dtype]
    except KeyError:
        raise KeyError(f"{dtype} must be one/list of either ('float', 'integer', 'bool','str', 'number', 'datetime', 'timedelta')")
