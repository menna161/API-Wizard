from __future__ import annotations
from inspect import getfullargspec
import pprint
import re
import json
from typing import Optional
from pydantic import BaseModel
from polyaxon_sdk.models.v1_hp_choice import V1HpChoice
from polyaxon_sdk.models.v1_hp_date_range import V1HpDateRange
from polyaxon_sdk.models.v1_hp_date_time_range import V1HpDateTimeRange
from polyaxon_sdk.models.v1_hp_geom_space import V1HpGeomSpace
from polyaxon_sdk.models.v1_hp_lin_space import V1HpLinSpace
from polyaxon_sdk.models.v1_hp_log_normal import V1HpLogNormal
from polyaxon_sdk.models.v1_hp_log_space import V1HpLogSpace
from polyaxon_sdk.models.v1_hp_log_uniform import V1HpLogUniform
from polyaxon_sdk.models.v1_hp_normal import V1HpNormal
from polyaxon_sdk.models.v1_hp_p_choice import V1HpPChoice
from polyaxon_sdk.models.v1_hp_q_log_normal import V1HpQLogNormal
from polyaxon_sdk.models.v1_hp_q_log_uniform import V1HpQLogUniform
from polyaxon_sdk.models.v1_hp_q_normal import V1HpQNormal
from polyaxon_sdk.models.v1_hp_q_uniform import V1HpQUniform
from polyaxon_sdk.models.v1_hp_range import V1HpRange
from polyaxon_sdk.models.v1_hp_uniform import V1HpUniform


@classmethod
def from_dict(cls, obj: dict) -> V1HpParams:
    'Create an instance of V1HpParams from a dict'
    if (obj is None):
        return None
    if (type(obj) is not dict):
        return V1HpParams.parse_obj(obj)
    _obj = V1HpParams.parse_obj({'choice': (V1HpChoice.from_dict(obj.get('choice')) if (obj.get('choice') is not None) else None), 'pchoice': (V1HpPChoice.from_dict(obj.get('pchoice')) if (obj.get('pchoice') is not None) else None), 'range': (V1HpRange.from_dict(obj.get('range')) if (obj.get('range') is not None) else None), 'linspace': (V1HpLinSpace.from_dict(obj.get('linspace')) if (obj.get('linspace') is not None) else None), 'logspace': (V1HpLogSpace.from_dict(obj.get('logspace')) if (obj.get('logspace') is not None) else None), 'geomspace': (V1HpGeomSpace.from_dict(obj.get('geomspace')) if (obj.get('geomspace') is not None) else None), 'uniform': (V1HpUniform.from_dict(obj.get('uniform')) if (obj.get('uniform') is not None) else None), 'quniform': (V1HpQUniform.from_dict(obj.get('quniform')) if (obj.get('quniform') is not None) else None), 'loguniform': (V1HpLogUniform.from_dict(obj.get('loguniform')) if (obj.get('loguniform') is not None) else None), 'qloguniform': (V1HpQLogUniform.from_dict(obj.get('qloguniform')) if (obj.get('qloguniform') is not None) else None), 'normal': (V1HpNormal.from_dict(obj.get('normal')) if (obj.get('normal') is not None) else None), 'qnormal': (V1HpQNormal.from_dict(obj.get('qnormal')) if (obj.get('qnormal') is not None) else None), 'lognormal': (V1HpLogNormal.from_dict(obj.get('lognormal')) if (obj.get('lognormal') is not None) else None), 'qlognormal': (V1HpQLogNormal.from_dict(obj.get('qlognormal')) if (obj.get('qlognormal') is not None) else None), 'daterange': (V1HpDateRange.from_dict(obj.get('daterange')) if (obj.get('daterange') is not None) else None), 'datetimerange': (V1HpDateTimeRange.from_dict(obj.get('datetimerange')) if (obj.get('datetimerange') is not None) else None)})
    return _obj
