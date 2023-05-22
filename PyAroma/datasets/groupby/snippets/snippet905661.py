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


def eval_op(op: RelationalOp) -> Optional[Table]:
    if (op.op_type == RelationalOpType.base):
        b_op = cast(BaseOp, op)
        return b_op.table
    else:
        prev_table = eval_op(op.child)
        if (not prev_table):
            return None
        if (op.op_type == RelationalOpType.where):
            s_op = cast(Where, op)
            new_table = prev_table.where(s_op.predicate.column_or_label, s_op.predicate.value_or_predicate, s_op.predicate.other)
            return new_table
        if (op.op_type == RelationalOpType.project):
            p_op = cast(Select, op)
            new_table = prev_table.select(p_op.columns)
            return new_table
        if (op.op_type == RelationalOpType.groupby):
            g_op = cast(GroupBy, op)
            new_table = prev_table.group(g_op.columns, g_op.collect)
            return new_table
        if (op.op_type == RelationalOpType.join):
            j_op = cast(Join, op)
            new_table = prev_table.join(j_op.self_columns, j_op.other.table, j_op.other_columns)
            return new_table
        else:
            raise NotImplementedError(op.op_type)
