from collections import defaultdict
from math import ceil
from copy import deepcopy
from typing import Union, Dict, List, Optional, Tuple, Callable, overload, NoReturn, Set, Iterable, Any, TypeVar, Type, Generator
import warnings
import numpy as np
from numpy import nan, ndarray
from . import _init_funcs as init
from . import _utils as utils
from . import options
from ._date import DateTimeClass, TimeDeltaClass
from ._libs import groupby as _gb, validate_arrays as _va, math as _math, math_oper_string as _mos, sort_rank as _sr, unique as _uq, replace as _repl, pivot as _pivot, out_files as _of, join as _join
from ._strings import StringClass
from . import _stat_funcs as _sf
from ._arithmetic_ops import Operations2D
from ._libs import math_oper
from ._groupby import Grouper
from ._rolling import Roller


def get_replacement(key, val):
    if isinstance(key, np.timedelta64):
        if (not isinstance(val, np.timedelta64)):
            raise TypeError(f'Cannot replace a timedelta64 with {type(val)}')
        dtype = 'm'
        dtype_conversion['m'] = 'm'
    elif isinstance(key, (bool, np.bool_)):
        if isinstance(val, (bool, np.bool_)):
            if (dtype_conversion.get('b', None) != 'f'):
                dtype_conversion['b'] = 'b'
        elif isinstance(val, (int, np.integer)):
            if (dtype_conversion.get('b', None) != 'f'):
                dtype_conversion['b'] = 'i'
        elif isinstance(val, (float, np.floating)):
            dtype_conversion['b'] = 'f'
        else:
            raise TypeError(f'Cannot replace a boolean with {type(val)}')
        dtype = 'b'
    elif isinstance(key, (int, np.integer)):
        if isinstance(val, (bool, np.bool_, int, np.integer)):
            dtype_conversion['i'] = 'i'
        elif isinstance(val, (float, np.floating)):
            dtype_conversion['i'] = 'f'
        else:
            raise TypeError(f'Cannot replace an integer with {type(val)}')
        dtype = 'i'
        dtype_conversion['f'] = 'f'
    elif isinstance(key, (float, np.floating)):
        if (not isinstance(val, (bool, np.bool_, int, np.integer, float, np.floating))):
            raise TypeError(f'Cannot replace a float with {type(val)}')
        dtype = 'f'
        dtype_conversion['f'] = 'f'
    elif (isinstance(key, str) or (key is None)):
        if ((not isinstance(val, str)) and (val is not None)):
            raise TypeError(f'Cannot replace a str with {type(val)}')
        dtype = 'S'
        dtype_conversion['S'] = 'S'
    elif isinstance(key, np.datetime64):
        if (not isinstance(val, np.datetime64)):
            raise TypeError(f'Cannot replace a datetime64 with {type(val)}')
        dtype = 'M'
        dtype_conversion['M'] = 'M'
    else:
        raise TypeError(f'Unknown replacement type: {type(key)}')
    specific_replacement[dtype].append((key, val))
    if (dtype == 'i'):
        specific_replacement['f'].append((key, val))
