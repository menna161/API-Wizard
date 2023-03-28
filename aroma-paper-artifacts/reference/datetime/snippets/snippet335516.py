from appdaemon.plugins.hass.hassapi import Hass
from appdaemontestframework import automation_fixture
import mock
import pytest
import datetime


def test_seconds(self, time_travel, automation_at_noon):
    time_travel.fast_forward(600).seconds()
    assert (automation_at_noon.datetime() == datetime.datetime(2020, 1, 1, 12, 10))
