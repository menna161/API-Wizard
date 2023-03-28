from appdaemon.plugins.hass.hassapi import Hass
from appdaemontestframework import automation_fixture
import mock
import pytest
import datetime


def callback(kwargs):
    nonlocal time_when_called
    time_when_called.append(automation.datetime())
