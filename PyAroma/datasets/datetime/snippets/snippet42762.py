from collections import defaultdict
from typing import Union, Dict, List, Optional, Tuple, Set
import numpy as np
from numpy import ndarray
from ._libs import validate_arrays as _va
from . import _utils


def data_from_dict(data: DataC) -> TupleReturn:
    '\n    Sets the _data attribute whenever a dictionary is passed to the `data` parameter in the\n    DataFrame constructor. Also sets `_column_info`\n\n    Parameters\n    ----------\n    data: Dictionary of lists or 1d arrays\n\n    Returns\n    -------\n    None\n    '
    column_info: ColInfoT = {}
    data_dict: DictListArr = defaultdict(list)
    str_reverse_map: StrReverse = {}
    for (i, (col, values)) in enumerate(data.items()):
        if isinstance(values, list):
            (arr, kind, srm) = _va.convert_object_array(values, col)
        elif isinstance(values, ndarray):
            arr = _utils.try_to_squeeze_array(values)
            kind = arr.dtype.kind
            if (kind == 'O'):
                (arr, kind, srm) = _va.convert_object_array(values, col)
            elif (kind == 'b'):
                arr = arr.astype('int8')
            elif (kind in 'SU'):
                arr = arr.astype('U')
                (arr, kind, srm) = _va.convert_str_to_cat(arr)
            elif (kind == 'M'):
                arr = arr.astype('datetime64[ns]')
            elif (kind == 'm'):
                arr = arr.astype('timedelta64[ns]')
        else:
            raise TypeError('Values of dictionary must be an array or a list')
        loc: int = len(data_dict.get(kind, []))
        data_dict[kind].append(arr)
        if (kind == 'S'):
            str_reverse_map[loc] = srm
        column_info[col] = _utils.Column(kind, loc, i)
        if (i == 0):
            first_len: int = len(arr)
        elif (len(arr) != first_len):
            raise ValueError('All columns must be the same length')
    return (concat_arrays(data_dict), column_info, str_reverse_map)
