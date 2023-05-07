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


def get_datetime_distribution_code(col_name, df):
    col_value = df.table.column(col_name)
    for h in DATE_HIERARCHY:
        r = try_parsing_date_time_level(h, col_value, col_name, df.df_name)
        if r:
            return (r, True, '')
    return ('', False, 'Cannot parse the date time column')
