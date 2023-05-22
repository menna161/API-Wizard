from copy import deepcopy, copy
from typing import List, Dict, Optional, cast, Tuple
from collections import defaultdict
from IPython.core.debugger import set_trace
from b2.util.errors import InternalLogicalError, debug_log
from b2.state_types import DFName
from b2.constants import ISDEBUG
from .dataframe import RelationalOpType, MidasDataFrame, BaseOp, RelationalOp, DFInfo, VisualizedDFInfo, Where, JoinInfo, Select, create_predicate, Join
from .selection import SelectionValue


def get_base_df_selection(self, s: SelectionValue) -> Optional[SelectionValue]:
    df = self.get_df(s.column.df_name)
    bases = find_all_baseops(df._ops)

    def find_base_with_column(bases: List[BaseOp]):
        for b in bases:
            a_df = self.get_df(b.df_name)
            if (s.column.col_name in a_df.table.labels):
                return b
    base_op = find_base_with_column(bases)
    new_selection = deepcopy(s)
    if base_op:
        new_selection.column.df_name = base_op.df_name
        return new_selection
    else:
        return None
