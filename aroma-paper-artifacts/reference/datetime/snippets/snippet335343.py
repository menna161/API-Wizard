from datetime import time, datetime
import appdaemon.plugins.hass.hassapi as hass
import pytest
from pytest import mark
from appdaemontestframework import automation_fixture


def test_failure__wrong_time(self, automation: MockAutomation, assert_that):
    automation.enable_register_run_at_during_initialize()
    with pytest.raises(AssertionError):
        assert_that(automation).registered.run_at(datetime(2019, 11, 5, 20, 43, 0, 0), extra_param='ok').with_callback(automation._my_run_at_callback)
