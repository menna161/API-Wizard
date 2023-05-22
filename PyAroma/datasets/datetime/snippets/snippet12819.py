import datetime
import functools
import json
import uuid
from decimal import Decimal
from enum import Enum, IntEnum
from typing import TYPE_CHECKING, Any, Optional
from typing import Any, Optional, Type, TypeVar, Union
from uuid import UUID
import ciso8601
from postmodel.exceptions import ConfigurationError, NoValuesFetched, OperationalError, FieldValueError


def __init__(self, auto_now: bool=False, auto_now_add: bool=False, **kwargs) -> None:
    if (auto_now_add and auto_now):
        raise ConfigurationError("You can choose only 'auto_now' or 'auto_now_add'")
    super().__init__(datetime.datetime, **kwargs)
    self.auto_now = auto_now
    self.auto_now_add = (auto_now | auto_now_add)
