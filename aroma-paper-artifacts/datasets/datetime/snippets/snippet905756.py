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


def try_parsing_date_time_level(ref, col_value, col_name, df_name):
    parsed = col_value.astype(f'datetime64[{ref[0]}]')
    count = len(np.unique(parsed))
    new_col_name = sanitize_string_for_var_name(f'{col_name}_{ref[1]}')
    if (count > 1):
        new_column = f"{df_name}['{col_name}_{ref[1]}'] = {df_name}['{col_name}'].astype('datetime64[{ref[0]}]')"
        new_name = f'{df_name}_{new_col_name}_dist'
        if (count > MAX_BINS):
            bound = snap_to_nice_number((count / MAX_BINS))
            binning_lambda = f"lambda x: 'null' if np.isnan(x) else int(x/{bound}) * {bound}"
            bin_column_name = f'{new_col_name}_bin'
            bin_transform = f"{df_name}['{bin_column_name}'] = {df_name}.apply({binning_lambda}, '{col_name}')"
            grouping = get_basic_group_vis(new_name, df_name, new_col_name)
            code = f'''{new_column}
{bin_transform}
{grouping}'''
            return code
        else:
            grouping = get_basic_group_vis(new_name, df_name, new_col_name)
            code = f'''{new_column}
{grouping}'''
            return code
    else:
        return None
