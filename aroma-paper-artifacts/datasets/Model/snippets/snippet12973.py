import pytest
from datetime import datetime, date, timedelta
import json
import uuid
import time
from tests.testmodels import IntFieldsModel, DataVersionFieldsModel, DatetimeFieldsModel, DateFieldsModel, TimeDeltaFieldsModel, JSONFieldsModel, UUIDFieldsModel
from postmodel.models.fields import BinaryField, CharField, DecimalField, DatetimeField, UUIDField
from postmodel.exceptions import ConfigurationError, FieldValueError


def test_dataversion_field():
    model = DataVersionFieldsModel(id=1)
    assert (model.data_ver == 0)
    fields_map = model._meta.fields_map
    data_ver = fields_map['data_ver']
    data_ver.auto_value(model)
    assert (model.data_ver == 1)
