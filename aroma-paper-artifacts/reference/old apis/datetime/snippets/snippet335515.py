from appdaemon.plugins.hass.hassapi import Hass
from appdaemontestframework import automation_fixture
import mock
import pytest
import datetime


@staticmethod
@pytest.fixture
def automation_at_noon(automation, time_travel, given_that):
    given_that.time_is(datetime.datetime(2020, 1, 1, 12, 0))
    return automation
