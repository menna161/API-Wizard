from datascience import Table
import json
import numpy as np
from math import log10, pow, floor
from pandas import notnull
from typing import Tuple
from IPython.core.debugger import set_trace
from b2.constants import IS_OVERVIEW_FIELD_NAME, MAX_BINS, STUB_DISTRIBUTION_BIN, MAX_GENERATED_BINS
from b2.vis_types import FilterLabelOptions, EncodingSpec
from .errors import InternalLogicalError
from .utils import sanitize_string_for_var_name
import numpy as np


def sanitize_dataframe(df: Table):
    'Sanitize a DataFrame to prepare it for serialization.\n    \n    copied from the ipyvega project\n    * Make a copy\n    * Convert categoricals to strings.\n    * Convert np.bool_ dtypes to Python bool objects\n    * Convert np.int dtypes to Python int objects\n    * Convert floats to objects and replace NaNs/infs with None.\n    * Convert DateTime dtypes into appropriate string representations\n    '
    import numpy as np
    if (df is None):
        return None
    df = df.copy()

    def to_list_if_array(val):
        if isinstance(val, np.ndarray):
            return val.tolist()
        else:
            return val
    for col_name in df.labels:
        dtype = df.column(col_name).dtype
        if (str(dtype) == 'category'):
            df[col_name] = df[col_name].astype(str)
        elif (str(dtype) == 'bool'):
            df[col_name] = df[col_name].astype(object)
        elif np.issubdtype(dtype, np.integer):
            df[col_name] = df[col_name].astype(object)
        elif np.issubdtype(dtype, np.floating):
            col = df[col_name]
            bad_values = (np.isnan(col) | np.isinf(col))
            df[col_name] = np.where(bad_values, None, col).astype(object)
        elif str(dtype).startswith('datetime'):
            new_column = df[col_name].astype(str)
            new_column[(new_column == 'NaT')] = ''
            df[col_name] = new_column
        elif (dtype == object):
            col = np.vectorize(to_list_if_array)(df[col_name])
            df[col_name] = np.where(notnull(col), col, None).astype(object)
    return df
