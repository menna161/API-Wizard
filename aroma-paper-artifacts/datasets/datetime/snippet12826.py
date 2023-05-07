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


def to_db_value(self, value: Optional[datetime.timedelta]) -> Optional[int]:
    if (value is None):
        return None
    return (((value.days * 86400000000) + (value.seconds * 1000000)) + value.microseconds)
