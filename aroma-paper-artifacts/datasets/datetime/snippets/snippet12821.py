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


def auto_value(self, model_instance):
    current_value = getattr(model_instance, self.model_field_name)
    if (self.auto_now or (self.auto_now_add and (current_value is None))):
        value = datetime.datetime.utcnow()
        setattr(model_instance, self.model_field_name, value)
