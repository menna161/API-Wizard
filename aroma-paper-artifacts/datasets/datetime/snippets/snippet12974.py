import pytest
from datetime import datetime, date, timedelta
import json
import uuid
import time
from tests.testmodels import IntFieldsModel, DataVersionFieldsModel, DatetimeFieldsModel, DateFieldsModel, TimeDeltaFieldsModel, JSONFieldsModel, UUIDFieldsModel
from postmodel.models.fields import BinaryField, CharField, DecimalField, DatetimeField, UUIDField
from postmodel.exceptions import ConfigurationError, FieldValueError


def test_datatime_field():
    model = DatetimeFieldsModel(id=1, datetime=datetime.utcnow())
    fields_map = model._meta.fields_map
    field = fields_map['datetime']
    fields_map['datetime_null'].auto_value(model)
    assert (model.datetime_null == None)
    assert (field.to_python_value(None) == None)
    dt = datetime.now()
    assert (field.to_python_value(dt) == dt)
    assert (field.to_python_value('2020-01-06 12:12:12') == datetime(2020, 1, 6, 12, 12, 12))
    assert (model.datetime_auto == None)
    assert (model.datetime_add == None)
    dt = datetime.utcnow()
    time.sleep(1)
    fields_map['datetime_auto'].auto_value(model)
    fields_map['datetime_add'].auto_value(model)
    assert (model.datetime_auto > dt)
    assert (model.datetime_add > dt)
