from copy import deepcopy, copy
from typing import List, Dict, Optional, cast, Tuple
from collections import defaultdict
from IPython.core.debugger import set_trace
from b2.util.errors import InternalLogicalError, debug_log
from b2.state_types import DFName
from b2.constants import ISDEBUG
from .dataframe import RelationalOpType, MidasDataFrame, BaseOp, RelationalOp, DFInfo, VisualizedDFInfo, Where, JoinInfo, Select, create_predicate, Join
from .selection import SelectionValue


def apply_selection_from_single_df(self, ops: RelationalOp, df_name: DFName, selections: List[SelectionValue]) -> RelationalOp:
    bases = find_all_baseops(ops)
    non_join_base_list = list(filter((lambda b: (b.df_name == df_name)), bases))
    if (len(non_join_base_list) > 0):
        non_join_base = non_join_base_list[0]
        local_base_df_name = non_join_base.df_name
        replacement_op = apply_non_join_selection(non_join_base, selections)
    else:
        r = self.find_joinable_base(bases, df_name)
        if r:
            local_base_df_name = r.left_df.df_name
            replacement_op = self.apply_join_selection(r, selections)
        else:
            if ISDEBUG:
                debug_log(f'No op for {df_name} selection because no join was found')
            return ops
    if (replacement_op and local_base_df_name):
        return set_if_eq(deepcopy(ops), replacement_op, local_base_df_name)
    raise InternalLogicalError('Replacement Op is not set or the df_name is not set')
