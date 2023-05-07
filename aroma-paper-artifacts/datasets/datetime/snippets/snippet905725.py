from enum import Enum
from functools import reduce
from typing import List, Union, Optional, NamedTuple, Set, cast, Callable, Any
from datetime import datetime
import inspect
import asttokens
import ast
import operator
from datascience import Table, are
import numpy as np
from pandas import DataFrame
from vega import VegaLite
from IPython.core.debugger import set_trace
from b2.constants import MAX_BINS, MAX_DOTS, ISDEBUG
from b2.state_types import DFName
from b2.vis_types import EncodingSpec
from b2.util.errors import InternalLogicalError, UserError, NotAllCaseHandledError
from b2.util.utils import find_name, find_tuple_name, get_random_string, plot_heatmap, red_print
from b2.util.errors import type_check_with_warning, InternalLogicalError
from b2.vis_types import EncodingSpec, ENCODING_COUNT
from b2.showme import infer_encoding_helper
from b2.util.data_processing import static_vega_gen
from .selection import SelectionType, SelectionValue, NumericRangeSelection, SetSelection, ColumnRef
from .data_types import DFId


def __init__(self, df: MidasDataFrame):
    if (not df.df_name):
        raise InternalLogicalError('Visualized dfs must have df_names')
    self.df = df
    self.created_on = datetime.now()
    self.df_name = df.df_name
    self.original_df = df
    self.df_type = 'visualized'