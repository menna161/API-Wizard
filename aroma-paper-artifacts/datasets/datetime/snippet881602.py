from __future__ import annotations
from inspect import getfullargspec
import pprint
import re
import json
from typing import Optional
from pydantic import BaseModel
from polyaxon_sdk.models.v1_cron_schedule import V1CronSchedule
from polyaxon_sdk.models.v1_date_time_schedule import V1DateTimeSchedule
from polyaxon_sdk.models.v1_interval_schedule import V1IntervalSchedule


def to_dict(self):
    'Returns the dictionary representation of the model using alias'
    _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
    if self.cron:
        _dict['cron'] = self.cron.to_dict()
    if self.datetime:
        _dict['datetime'] = self.datetime.to_dict()
    if self.interval:
        _dict['interval'] = self.interval.to_dict()
    return _dict
