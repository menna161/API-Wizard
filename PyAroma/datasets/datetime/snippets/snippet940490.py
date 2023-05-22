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


def start_rescheduling_timer(self, delay: T.Union[(float, int, datetime.datetime, datetime.timedelta)]=None) -> None:
    "This method registers a re-scheduling timer according to the\n        room's settings. delay, if given, overwrites the rescheduling_delay\n        configured for the room. If there is a timer running already,\n        it's replaced by a new one."
    self.cancel_rescheduling_timer()
    if (delay is None):
        delay = self.cfg['rescheduling_delay']
    if isinstance(delay, (float, int)):
        delta = datetime.timedelta(minutes=delay)
        when = (self.app.datetime() + delta)
    elif isinstance(delay, datetime.datetime):
        delta = (delay - self.app.datetime())
        when = delay
    elif isinstance(delay, datetime.timedelta):
        delta = delay
        when = (self.app.datetime() + delay)
    self.log('Re-applying the schedule not before {} (in {}).'.format(util.format_time(when.time()), delta))
    with self._timer_lock:
        self._rescheduling_time = when
        self._rescheduling_timer = self.app.run_at(self._rescheduling_timer_cb, when)
