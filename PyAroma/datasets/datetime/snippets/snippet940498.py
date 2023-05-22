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


def _restore_overlaid_value() -> bool:
    'Restores and clears an overlaid value.\n            Returns whether a value has actually been restored or not.'
    overlaid_wanted_value = self._overlaid_wanted_value
    if (overlaid_wanted_value is None):
        self.log('Overlay ended but knowing no value to restore.', level='WARNING')
        self._clear_overlay()
        return False
    delay = None
    if (not self._overlaid_rescheduling_time):
        if (new_scheduled_value == self._overlaid_scheduled_value):
            delay = 0
    elif (self._overlaid_rescheduling_time > self.app.datetime()):
        delay = self._overlaid_rescheduling_time
    else:
        self.log('Overlaid value {!r} has expired, not restoring it.'.format(overlaid_wanted_value))
    self._clear_overlay()
    if (delay is None):
        return False
    self.log('Restoring overlaid value {}.'.format(repr(overlaid_wanted_value)))
    self.set_value_manually(value=overlaid_wanted_value, rescheduling_delay=delay)
    return True
