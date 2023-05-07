from collections import defaultdict
from typing import Union, Dict, List, Optional, Tuple, Set
import numpy as np
from numpy import ndarray
from ._libs import validate_arrays as _va
from . import _utils


def data_from_typed_array(data: ndarray, columns: ndarray) -> TupleReturn:
    '\n    Stores entire array, `data` into `self._data` as one kind\n\n    Parameters\n    ----------\n    data : A homogeneous array\n    columns: Array\n\n    Returns\n    -------\n    None\n    '
    kind: str = data.dtype.kind
    str_reverse_map: StrReverse = {}
    if (data.ndim == 1):
        data = data[(:, np.newaxis)]
    if (kind in 'OSU'):
        kind = 'S'
        (data, col_str_map) = _va.convert_str_to_cat_2d(data)
        str_reverse_map = {0: list(col_str_map)}
    elif (kind == 'M'):
        data = data.astype('datetime64[ns]')
    elif (kind == 'm'):
        data = data.astype('timedelta64[ns]')
    elif (kind == 'b'):
        data = data.astype('int8')
    new_data = {kind: np.asfortranarray(data)}
    column_info: ColInfoT = {col: _utils.Column(kind, i, i) for (i, col) in enumerate(columns)}
    return (new_data, column_info, str_reverse_map)
