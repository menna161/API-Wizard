from __future__ import annotations
from inspect import getfullargspec
import pprint
import re
import json
from typing import Any, Dict, Optional
from pydantic import BaseModel, StrictStr


@classmethod
def from_dict(cls, obj: dict) -> V1HpDateTimeRange:
    'Create an instance of V1HpDateTimeRange from a dict'
    if (obj is None):
        return None
    if (type(obj) is not dict):
        return V1HpDateTimeRange.parse_obj(obj)
    _obj = V1HpDateTimeRange.parse_obj({'kind': (obj.get('kind') if (obj.get('kind') is not None) else 'datetimerange'), 'value': obj.get('value')})
    return _obj
