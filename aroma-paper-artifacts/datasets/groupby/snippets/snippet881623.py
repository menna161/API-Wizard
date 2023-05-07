from __future__ import annotations
from inspect import getfullargspec
import pprint
import re
import json
from typing import Any, Dict, Optional
from pydantic import BaseModel, StrictInt, StrictStr
from polyaxon_sdk.models.v1_analytics_spec import V1AnalyticsSpec
from polyaxon_sdk.models.v1_dashboard_spec import V1DashboardSpec


@classmethod
def from_dict(cls, obj: dict) -> V1SearchSpec:
    'Create an instance of V1SearchSpec from a dict'
    if (obj is None):
        return None
    if (type(obj) is not dict):
        return V1SearchSpec.parse_obj(obj)
    _obj = V1SearchSpec.parse_obj({'query': obj.get('query'), 'sort': obj.get('sort'), 'limit': obj.get('limit'), 'offset': obj.get('offset'), 'groupby': obj.get('groupby'), 'columns': obj.get('columns'), 'layout': obj.get('layout'), 'sections': obj.get('sections'), 'compares': obj.get('compares'), 'heat': obj.get('heat'), 'events': (V1DashboardSpec.from_dict(obj.get('events')) if (obj.get('events') is not None) else None), 'histograms': obj.get('histograms'), 'trends': obj.get('trends'), 'analytics': (V1AnalyticsSpec.from_dict(obj.get('analytics')) if (obj.get('analytics') is not None) else None)})
    return _obj
