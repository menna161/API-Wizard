import typing as T
import datetime
import functools
from cached_property import cached_property
from . import util
from . import expression
import types
from .room import Room


def __init__(self, name: str=None, start_time: datetime.time=None, start_plus_days: int=None, end_time: datetime.time=None, end_plus_days: int=None, constraints: T.Dict[(str, T.Any)]=None, expr: 'types.CodeType'=None, expr_raw: str=None, value: T.Any=None) -> None:
    _checks = [(expr is None), (expr_raw is None)]
    if (any(_checks) and (not all(_checks))):
        raise ValueError('expr and expr_raw may only be passed together')
    if ((expr is not None) and (value is not None)):
        raise ValueError('specify only one of expr and value, not both')
    self.name = name
    self.start_time = start_time
    self.start_plus_days = start_plus_days
    self.end_time = end_time
    self.end_plus_days = end_plus_days
    if (constraints is None):
        constraints = {}
    self.constraints = constraints
    self.expr = expr
    self.expr_raw = expr_raw
    self.value = value
    self.check_constraints = functools.lru_cache(maxsize=64)(self._check_constraints)
