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


def get_midas_code(op: RelationalOp, midas_reference_name: str) -> str:
    if (op.op_type == RelationalOpType.base):
        b_op = cast(BaseOp, op)
        return b_op.df_name
    else:
        prev_table = get_midas_code(op.child, midas_reference_name)
        if (op.op_type == RelationalOpType.where):
            s_op = cast(Where, op)
            col_or_label = convert_value_or_predicate(s_op.predicate.column_or_label, midas_reference_name)
            val_or_pred = convert_value_or_predicate(s_op.predicate.value_or_predicate, midas_reference_name)
            if (s_op.predicate.other is None):
                return f'{prev_table}.where({col_or_label}, {val_or_pred})'
            else:
                other = convert_value_or_predicate(s_op.predicate.other, midas_reference_name)
                return f'{prev_table}.where({col_or_label}, {val_or_pred}, {other})'
        if (op.op_type == RelationalOpType.project):
            p_op = cast(Select, op)
            new_table = f'{prev_table}.select({p_op.columns!r})'
            return new_table
        if (op.op_type == RelationalOpType.groupby):
            g_op = cast(GroupBy, op)
            if (g_op.collect is None):
                return f'{prev_table}.group({g_op.columns!r})'
            else:
                group_fun = get_lambda_declaration_or_fn_name(g_op.collect)
                return f'{prev_table}.group({g_op.columns!r}, {group_fun})'
        if (op.op_type == RelationalOpType.join):
            j_op = cast(Join, op)
            join_prep_code = ''
            if (j_op.other.df_name is not None):
                other_df_name = j_op.other.df_name
            else:
                if (not (hasattr(j_op.other, '_suggested_df_name') or hasattr(j_op.other._suggested_df_name, '_suggested_df_name'))):
                    raise InternalLogicalError('the join df should have a suggested name')
                ops_code = get_midas_code(j_op.other._ops, midas_reference_name)
                join_prep_code = f'{j_op.other._suggested_df_name} = {ops_code}'
                other_df_name = j_op.other._suggested_df_name
            new_table = f'''{join_prep_code}
{prev_table}.join({j_op.self_columns!r}, {other_df_name}, {j_op.other_columns!r})'''
            return new_table
        else:
            raise NotImplementedError(op.op_type)
