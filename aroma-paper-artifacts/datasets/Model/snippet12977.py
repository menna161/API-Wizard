import pytest
from datetime import datetime, date, timedelta
import json
import uuid
import time
from tests.testmodels import IntFieldsModel, DataVersionFieldsModel, DatetimeFieldsModel, DateFieldsModel, TimeDeltaFieldsModel, JSONFieldsModel, UUIDFieldsModel
from postmodel.models.fields import BinaryField, CharField, DecimalField, DatetimeField, UUIDField
from postmodel.exceptions import ConfigurationError, FieldValueError


def test_json_field():
    model = JSONFieldsModel(id=1, data={'fookey': 'hello', 'key2': 124})
    fields_map = model._meta.fields_map
    field = fields_map['data']
    assert (field.to_python_value(None) == None)
    assert (field.to_python_value(['a', 'b']) == ['a', 'b'])
    assert (field.to_python_value('["abc", 123, "cde"]') == ['abc', 123, 'cde'])
    assert (field.to_db_value(None) == None)
    assert (json.loads(field.to_db_value({'fookey': 'world', 'key2': 223})) == {'fookey': 'world', 'key2': 223})
