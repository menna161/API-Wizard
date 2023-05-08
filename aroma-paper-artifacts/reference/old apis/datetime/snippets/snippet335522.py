from appdaemon.plugins.hass.hassapi import Hass
from appdaemontestframework import automation_fixture
import mock
import pytest
import datetime


def test_time_is_correct_when_callback_it_run(self, time_travel, given_that, automation):
    given_that.time_is(datetime.datetime(2020, 1, 1, 12, 0))
    time_when_called = []

    def callback(kwargs):
        nonlocal time_when_called
        time_when_called.append(automation.datetime())
    automation.run_in(callback, 1)
    automation.run_in(callback, 15)
    automation.run_in(callback, 65)
    time_travel.fast_forward(90).seconds()
    expected_call_times = [datetime.datetime(2020, 1, 1, 12, 0, 1), datetime.datetime(2020, 1, 1, 12, 0, 15), datetime.datetime(2020, 1, 1, 12, 1, 5)]
    assert (expected_call_times == time_when_called)
