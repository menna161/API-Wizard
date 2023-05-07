import decimal
from typing import List, Dict, Set, Any, Union, Tuple, Iterable
import numpy as np
from numpy import ndarray
from ._libs import validate_arrays as va


def get_datetime_str(arr: ndarray):
    dt = {0: 'ns', 1: 'us', 2: 'ms', 3: 's', 4: 'D'}
    arr = arr[(~ np.isnat(arr))].view('int64')
    counts = np.zeros(len(arr), dtype='int64')
    for (i, val) in enumerate(arr):
        if (val == 0):
            counts[i] = 4
            continue
        dec = decimal.Decimal(int(val)).as_tuple()
        ct = 0
        for digit in dec.digits[::(- 1)]:
            if (digit == 0):
                ct += 1
            else:
                break
        if (ct >= 11):
            counts[i] = 4
        else:
            counts[i] = (ct // 3)
    return dt[counts.min()]
