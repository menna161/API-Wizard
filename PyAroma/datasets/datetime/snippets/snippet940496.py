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


def _serialize_dt(value: T.Optional[datetime.datetime]) -> T.Optional[float]:
    if (value is None):
        return None
    return value.timestamp()
