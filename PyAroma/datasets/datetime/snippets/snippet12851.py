from copy import copy, deepcopy
from collections.abc import Iterable
from postmodel.exceptions import ConfigurationError, OperationalError, StaleObjectError
from postmodel.exceptions import PrimaryKeyChangedError, PrimaryKeyIntegrityError
from postmodel.main import Postmodel
from collections import OrderedDict
from .query import QuerySet, FilterBuilder
from .fields import Field, DataVersionField
import re
import datetime
import uuid
import json


def to_jsondict(self):
    json_data = dict()
    for key in self._meta.fields_db_projection.keys():
        value = deepcopy(getattr(self, key))
        if isinstance(value, (datetime.date, datetime.datetime)):
            json_data[key] = value.isoformat()
        elif isinstance(value, uuid.UUID):
            json_data[key] = str(value)
        else:
            json_data[key] = value
    return json_data
