import logging
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.relationships import RelationshipProperty
from functools import partial
import isodate
from .custom.format import parse_time, parse_date
from collections import OrderedDict
from jsonschema import validate
from . import InvalidStatus
import pytz


def datetime_rfc3339(ob):
    if ob.tzinfo:
        return ob.isoformat()
    return pytz.utc.localize(ob).isoformat()
