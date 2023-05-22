from copy import deepcopy, copy
from typing import List, Dict, Optional, cast, Tuple
from collections import defaultdict
from IPython.core.debugger import set_trace
from b2.util.errors import InternalLogicalError, debug_log
from b2.state_types import DFName
from b2.constants import ISDEBUG
from .dataframe import RelationalOpType, MidasDataFrame, BaseOp, RelationalOp, DFInfo, VisualizedDFInfo, Where, JoinInfo, Select, create_predicate, Join
from .selection import SelectionValue


def find_all_baseops(op: RelationalOp) -> List[BaseOp]:
    'takes the source op and returns all the baseops\n       e.g. given that df and df2 are loaded in as external data,\n            then the op representing `df.join("id", df2, "id")select(["sales"])`\n            will return df and df2\'s respective `baseop`s.\n    \n    Arguments:\n        op {RelationalOp} -- [description]\n    \n    Returns:\n        List[BaseOp] -- [description]\n    '
    if (op.op_type == RelationalOpType.base):
        base_op = cast(BaseOp, op)
        return [base_op]
    if (op.op_type == RelationalOpType.join):
        join_op = cast(Join, op)
        b1 = find_all_baseops(op.child)
        b2 = find_all_baseops(join_op.other._ops)
        return (b1 + b2)
    if op.has_child():
        return find_all_baseops(op.child)
    else:
        return []
