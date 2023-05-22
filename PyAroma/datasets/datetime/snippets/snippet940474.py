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


def _restore_state(self) -> None:
    'Restores a stored state from Home Assistant and.applies it.\n        If no state was found, the schedule is just applied.'

    def _deserialize(value: T.Any) -> T.Any:
        if (value is None):
            return None
        assert (self.app.actor_type is not None)
        return self.app.actor_type.deserialize_value(value)

    def _deserialize_dt(value: T.Any) -> T.Optional[datetime.datetime]:
        if (not isinstance(value, (float, int))):
            return None
        return datetime.datetime.fromtimestamp(value)
    entity_id = self._state_entity_id
    self.log('Loading state of {} from Home Assistant.'.format(repr(entity_id)), level='DEBUG', prefix=common.LOG_PREFIX_OUTGOING)
    state = self.app.get_state(entity_id, attribute='all')
    self.log('  = {}'.format(repr(state)), level='DEBUG', prefix=common.LOG_PREFIX_INCOMING)
    reset = False
    if isinstance(state, dict):
        attrs = state.get('attributes', {})
        actor_wanted_values = attrs.get('actor_wanted_values', {})
        for (entity_id, value) in actor_wanted_values.items():
            value = _deserialize(value)
            if (entity_id in self.actors):
                self.actors[entity_id].wanted_value = value
        self._wanted_value = _deserialize((state.get('state') or None))
        self._scheduled_value = _deserialize(attrs.get('scheduled_value'))
        self._rescheduling_time = _deserialize_dt(attrs.get('rescheduling_time'))
        self._overlay_active = (attrs.get('overlay_active') or False)
        self._overlaid_wanted_value = _deserialize(attrs.get('overlaid_wanted_value'))
        self._overlaid_scheduled_value = _deserialize(attrs.get('overlaid_scheduled_value'))
        self._overlaid_rescheduling_time = _deserialize_dt(attrs.get('overlaid_rescheduling_time'))
        if self._rescheduling_time:
            if (self._rescheduling_time > self.app.datetime()):
                if self.cfg['replicate_changes']:
                    self.set_value(self._wanted_value)
                self.start_rescheduling_timer(self._rescheduling_time)
            else:
                self._rescheduling_time = None
                reset = True
    self.apply_schedule(reset=reset)
