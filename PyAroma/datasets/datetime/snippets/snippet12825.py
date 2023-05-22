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


def to_python_value(self, value: Any) -> Optional[datetime.timedelta]:
    if ((value is None) or isinstance(value, datetime.timedelta)):
        return value
    return datetime.timedelta(microseconds=value)