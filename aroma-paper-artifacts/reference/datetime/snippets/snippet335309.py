from datetime import time, datetime
import appdaemon.plugins.hass.hassapi as hass
import pytest
from pytest import mark
from appdaemontestframework import automation_fixture


def initialize(self):
    if self.should_listen_state:
        self.listen_state(self._my_listen_state_callback, 'some_entity', new='off')
    if self.should_listen_event:
        self.listen_event(self._my_listen_event_callback, 'zwave.scene_activated', scene_id=3)
    if self.should_register_run_daily:
        self.run_daily(self._my_run_daily_callback, time(hour=3, minute=7), extra_param='ok')
    if self.should_register_run_minutely:
        self.run_minutely(self._my_run_minutely_callback, time(hour=3, minute=7), extra_param='ok')
    if self.should_register_run_at:
        self.run_at(self._my_run_at_callback, datetime(2019, 11, 5, 22, 43, 0, 0), extra_param='ok')
