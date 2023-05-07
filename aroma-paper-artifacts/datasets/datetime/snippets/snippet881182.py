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


def to_dict(self):
    'Returns the dictionary representation of the model using alias'
    _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
    if self.choice:
        _dict['choice'] = self.choice.to_dict()
    if self.pchoice:
        _dict['pchoice'] = self.pchoice.to_dict()
    if self.range:
        _dict['range'] = self.range.to_dict()
    if self.linspace:
        _dict['linspace'] = self.linspace.to_dict()
    if self.logspace:
        _dict['logspace'] = self.logspace.to_dict()
    if self.geomspace:
        _dict['geomspace'] = self.geomspace.to_dict()
    if self.uniform:
        _dict['uniform'] = self.uniform.to_dict()
    if self.quniform:
        _dict['quniform'] = self.quniform.to_dict()
    if self.loguniform:
        _dict['loguniform'] = self.loguniform.to_dict()
    if self.qloguniform:
        _dict['qloguniform'] = self.qloguniform.to_dict()
    if self.normal:
        _dict['normal'] = self.normal.to_dict()
    if self.qnormal:
        _dict['qnormal'] = self.qnormal.to_dict()
    if self.lognormal:
        _dict['lognormal'] = self.lognormal.to_dict()
    if self.qlognormal:
        _dict['qlognormal'] = self.qlognormal.to_dict()
    if self.daterange:
        _dict['daterange'] = self.daterange.to_dict()
    if self.datetimerange:
        _dict['datetimerange'] = self.datetimerange.to_dict()
    return _dict
