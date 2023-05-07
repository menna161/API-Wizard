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


def describe(self, percentiles: List[float]=[0.25, 0.5, 0.75], summary_type: str='numeric') -> 'DataFrame':
    '\n        Provides several summary statistics for each column\n        Parameters\n        ----------\n        percentiles\n        summary_type\n\n        Returns\n        -------\n\n        '
    if (summary_type == 'numeric'):
        df = self.select_dtypes('number')
    elif (summary_type == 'non-numeric'):
        df = self.select_dtypes(['str', 'bool', 'datetime'])
    else:
        raise ValueError('`summary_type` must be either "numeric" or "non-numeric"')
    data_dict: DictListArr = defaultdict(list)
    new_column_info: ColInfoT = {}
    new_columns: List[str] = []
    if (summary_type == 'numeric'):
        data_dict['S'].append(df._columns.copy('F'))
        new_column_info['Column Name'] = utils.Column('S', 0, 0)
        new_columns.append('Column Name')
        dtypes = df._get_dtype_list()
        data_dict['S'].append(dtypes)
        new_column_info['Data Type'] = utils.Column('S', 1, 1)
        new_columns.append('Data Type')
        funcs: List[Tuple[(str, Tuple[(str, Dict)])]] = [('count', ('i', {})), ('_null_pct', ('f', {})), ('mean', ('f', {})), ('std', ('f', {})), ('min', ('f', {}))]
        for perc in percentiles:
            funcs.append(('quantile', ('f', {'q': perc})))
        funcs.append(('max', ('f', {})))
        change_name: Dict[(str, Callable)] = {'_null_pct': (lambda x: 'null %'), 'quantile': (lambda x: f"{(x['q'] * 100):.2g}%")}
        order: int = 1
        for (func_name, (dtype, kwargs)) in funcs:
            loc: int = len(data_dict[dtype])
            order += 1
            value: ndarray = getattr(df, func_name)(**kwargs).values[0]
            data_dict[dtype].append(value)
            name = change_name.get(func_name, (lambda x: func_name))(kwargs)
            new_column_info[name] = utils.Column(dtype, loc, order)
            new_columns.append(name)
        new_data: Dict[(str, ndarray)] = init.concat_arrays(data_dict)
    else:
        raise NotImplementedError('non-numeric summary not available yet')
    return self._construct_from_new(new_data, new_column_info, np.asarray(new_columns, dtype='O'))
