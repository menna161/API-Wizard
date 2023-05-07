import pytest
from datetime import datetime, date, timedelta
import json
import uuid
import time
from tests.testmodels import IntFieldsModel, DataVersionFieldsModel, DatetimeFieldsModel, DateFieldsModel, TimeDeltaFieldsModel, JSONFieldsModel, UUIDFieldsModel
from postmodel.models.fields import BinaryField, CharField, DecimalField, DatetimeField, UUIDField
from postmodel.exceptions import ConfigurationError, FieldValueError


def test_uuid_field():
    f = UUIDField(pk=True)
    assert (f.default == uuid.uuid4)
    model = UUIDFieldsModel(data='123e4567-e89b-12d3-a456-426655440000')
    fields_map = model._meta.fields_map
    field = fields_map['data']
    v = uuid.uuid4()
    assert (field.to_python_value(None) == None)
    assert (field.to_python_value(v) == uuid.UUID(str(v)))
    assert (field.to_python_value(str(v)) == v)
    assert (field.to_db_value(None) == None)
    assert (field.to_db_value(v) == str(v))
