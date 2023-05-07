import pytest
from datetime import datetime, date, timedelta
import json
import uuid
import time
from tests.testmodels import IntFieldsModel, DataVersionFieldsModel, DatetimeFieldsModel, DateFieldsModel, TimeDeltaFieldsModel, JSONFieldsModel, UUIDFieldsModel
from postmodel.models.fields import BinaryField, CharField, DecimalField, DatetimeField, UUIDField
from postmodel.exceptions import ConfigurationError, FieldValueError


def test_date_field():
    model = DateFieldsModel(id=1, date=date.today())
    fields_map = model._meta.fields_map
    field = fields_map['date']
    assert (field.to_python_value(None) == None)
    dt = date.today()
    assert (field.to_python_value(dt) == dt)
    assert (field.to_python_value('2020-01-06') == date(2020, 1, 6))
