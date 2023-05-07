from __future__ import annotations
from inspect import getfullargspec
import pprint
import re
import json
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, StrictStr


@classmethod
def from_dict(cls, obj: dict) -> V1DateTimeSchedule:
    'Create an instance of V1DateTimeSchedule from a dict'
    if (obj is None):
        return None
    if (type(obj) is not dict):
        return V1DateTimeSchedule.parse_obj(obj)
    _obj = V1DateTimeSchedule.parse_obj({'kind': (obj.get('kind') if (obj.get('kind') is not None) else 'datetime'), 'start_at': obj.get('startAt')})
    return _obj
