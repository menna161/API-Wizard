import types
import typing as T
import datetime
import functools
import os
import threading
import traceback
from .. import common
from . import expression, util
import uuid
from .app import SchedyApp
from .schedule import Schedule
from .actor.base import ActorBase


def _deserialize_dt(value: T.Any) -> T.Optional[datetime.datetime]:
    if (not isinstance(value, (float, int))):
        return None
    return datetime.datetime.fromtimestamp(value)
