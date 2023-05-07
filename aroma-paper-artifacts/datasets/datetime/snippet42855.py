import decimal
from typing import List, Dict, Set, Any, Union, Tuple, Iterable
import numpy as np
from numpy import ndarray
from ._libs import validate_arrays as va


def is_scalar(value: Any) -> bool:
    return (isinstance(value, (int, str, float, np.number, bool, bytes, np.datetime64, np.timedelta64)) or (value is None))
