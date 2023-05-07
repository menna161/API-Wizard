import pytest
from datetime import datetime, date, timedelta
import json
import uuid
import time
from tests.testmodels import IntFieldsModel, DataVersionFieldsModel, DatetimeFieldsModel, DateFieldsModel, TimeDeltaFieldsModel, JSONFieldsModel, UUIDFieldsModel
from postmodel.models.fields import BinaryField, CharField, DecimalField, DatetimeField, UUIDField
from postmodel.exceptions import ConfigurationError, FieldValueError


def test_timedelta_field():
    model = TimeDeltaFieldsModel(id=1, timedelta=1000000)
    fields_map = model._meta.fields_map
    field = fields_map['timedelta']
    assert (field.to_python_value(None) == None)
    assert (field.to_python_value(timedelta(20, 0, 0)) == timedelta(20, 0, 0))
    assert (field.to_python_value(1000) == timedelta(microseconds=1000))
    assert (field.to_db_value(None) == None)
    assert (field.to_db_value(timedelta(days=1)) == (86400 * 1000000))
