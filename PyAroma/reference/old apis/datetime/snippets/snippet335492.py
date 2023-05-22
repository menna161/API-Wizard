from appdaemontestframework.appdaemon_mock.scheduler import MockScheduler
from appdaemontestframework.appdaemon_mock.appdaemon import MockAppDaemon
import asyncio
import pytest
import mock
import datetime
import pytz


def test_set_start_time_to_known_time(self, scheduler):
    new_time = datetime.datetime(2010, 6, 1, 0, 0)
    scheduler.sim_set_start_time(new_time)
    assert (scheduler.get_now_sync() == pytz.utc.localize(new_time))
