from appdaemontestframework.appdaemon_mock.scheduler import MockScheduler
from appdaemontestframework.appdaemon_mock.appdaemon import MockAppDaemon
import asyncio
import pytest
import mock
import datetime
import pytz


def test_fast_forward_to_past_raises_exception(self, scheduler):
    with pytest.raises(ValueError) as cm:
        scheduler.sim_fast_forward(datetime.timedelta((- 1)))
    assert (str(cm.value) == 'You can not fast forward to a time in the past.')
