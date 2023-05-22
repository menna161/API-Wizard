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


def _update_state(self) -> None:
    "Update the room's state in Home Assistant."
    D = T.TypeVar('D')

    def _serialize(value: T.Any, default: D) -> T.Union[(str, D)]:
        if (value is None):
            return default
        assert (self.app.actor_type is not None)
        return self.app.actor_type.serialize_value(value)

    def _serialize_dt(value: T.Optional[datetime.datetime]) -> T.Optional[float]:
        if (value is None):
            return None
        return value.timestamp()

    def _maybe_add(key: str, value: T.Any) -> None:
        if (value is not None):
            attrs[key] = value
    state = _serialize(self._wanted_value, '')
    attrs = {'actor_wanted_values': {entity_id: _serialize(actor.wanted_value, None) for (entity_id, actor) in self.actors.items()}, 'scheduled_value': _serialize(self._scheduled_value, None), 'rescheduling_time': _serialize_dt(self._rescheduling_time), 'overlay_active': self._overlay_active}
    _maybe_add('overlaid_wanted_value', _serialize(self._overlaid_wanted_value, None))
    _maybe_add('overlaid_scheduled_value', _serialize(self._overlaid_scheduled_value, None))
    _maybe_add('overlaid_rescheduling_time', _serialize_dt(self._overlaid_rescheduling_time))
    _maybe_add('friendly_name', self.cfg.get('friendly_name'))
    unchanged = ((state, attrs) == self._last_state)
    if unchanged:
        self.log('Unchanged HA state: state={}, attributes={}'.format(repr(state), attrs), level='DEBUG')
        return
    self.log('Sending state to HA: state={}, attributes={}'.format(repr(state), attrs), level='DEBUG', prefix=common.LOG_PREFIX_OUTGOING)
    entity_id = self._state_entity_id
    self.app.set_state(entity_id, state=state, attributes=attrs)
    self._last_state = (state, attrs)
