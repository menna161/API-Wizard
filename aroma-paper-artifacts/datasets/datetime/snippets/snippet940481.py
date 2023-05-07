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


@sync_proxy
def apply_schedule(self, reset: bool=False, force_resend: bool=False) -> None:
    "Applies the value scheduled for the current date and time.\n        It detects when the result hasn't changed compared to the last\n        run and prevent re-setting it in that case.\n        This method will also not re-apply the schedule if a re-schedule\n        timer runs - however, the OVERLAY marker is regarded.\n        These both checks can be skipped by setting reset to True.\n        force_resend is passed through to set_value()."

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
    self.log("Evaluating room's schedule (reset={}, force_resend={}).".format(reset, force_resend), level='DEBUG')
    result = None
    if self.schedule:
        result = self.schedule.evaluate(self, self.app.datetime())
    if (result is None):
        self.log('No suitable value found in schedule.', level='DEBUG')
        if self._overlay_active:
            new_scheduled_value = self._overlaid_scheduled_value
            _restore_overlaid_value()
            self._scheduled_value = new_scheduled_value
        return
    (new_scheduled_value, markers) = result[:2]
    if (not ((new_scheduled_value != self._scheduled_value) or ((not self._overlay_active) and (expression.types.Mark.OVERLAY in markers)) or (self._overlay_active and (expression.types.Mark.OVERLAY not in markers)) or reset or force_resend)):
        self.log("Result didn't change, not setting it again.", level='DEBUG')
        return
    if reset:
        self.cancel_rescheduling_timer()
        self._clear_overlay()
    elif (expression.types.Mark.OVERLAY in markers):
        self._store_for_overlaying()
    elif (self._overlay_active and _restore_overlaid_value()):
        self._scheduled_value = new_scheduled_value
        return
    elif self._rescheduling_timer:
        self.log('Not applying the schedule now due to a running re-scheduling timer.', level='DEBUG')
        return
    self._scheduled_value = new_scheduled_value
    self.set_value(new_scheduled_value, force_resend=force_resend)
