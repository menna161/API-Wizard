from datetime import datetime
from IPython import get_ipython
from pandas.api.types import is_string_dtype, is_numeric_dtype, is_datetime64_any_dtype
from ipykernel.comm import Comm
import numpy as np
from typing import Dict, Callable, Optional, List, Tuple, Type, cast
import json
from pyperclip import copy
import ast
import functools
import inspect
from IPython.core.debugger import set_trace
from .constants import ISDEBUG
from .algebra.data_types import DFId
from .algebra.dataframe import MidasDataFrame, RelationalOp, DFInfo, VisualizedDFInfo, get_midas_code
from .algebra.selection import SelectionValue, NumericRangeSelection, SetSelection, ColumnRef, EmptySelection
from .constants import MIDAS_CELL_COMM_NAME, MAX_BINS, MIDAS_RECOVERY_COMM_NAME, STUB_DISTRIBUTION_BIN
from .state_types import DFName
from .util.errors import InternalLogicalError, MockComm, debug_log, NotAllCaseHandledError
from .util.utils import sanitize_string_for_var_name
from .vis_types import EncodingSpec, FilterLabelOptions
from .util.data_processing import dataframe_to_dict, get_numeric_distribution_code, get_datetime_distribution_code, get_basic_group_vis


def create_distribution_query(self, col_name: str, df_name: str) -> Tuple[(str, bool, str)]:
    df_info = self.get_df(DFName(df_name))
    if (df_info is None):
        raise InternalLogicalError('Should not be getting distribution on unregistered dataframes and columns')
    df = df_info.df
    col_value = df.table.column(col_name)
    new_name = sanitize_string_for_var_name(f'{col_name}_{df_name}_dist')
    if is_string_dtype(col_value):
        code = get_basic_group_vis(new_name, df.df_name, col_name)
        try:
            unique_vals = np.unique(col_value)
        except TypeError:
            return (code, False, f'Please handle None values from {col_name}!')
        current_max_bins = len(unique_vals)
        if (current_max_bins < MAX_BINS):
            return (code, True, '')
        else:
            try:
                parsed = col_value.astype('datetime64')
                return get_datetime_distribution_code(col_name, df)
            except ValueError:
                return (code, False, f'Too many columns to display for column {col_name}!')
    else:
        unique_vals = np.unique(col_value[(~ np.isnan(col_value))])
        current_max_bins = len(unique_vals)
        if (current_max_bins < MAX_BINS):
            code = get_basic_group_vis(new_name, df.df_name, col_name)
            return (code, True, '')
        else:
            return get_numeric_distribution_code(current_max_bins, unique_vals, col_name, df.df_name, new_name, self.midas_instance_name)
