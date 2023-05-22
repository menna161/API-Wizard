import datetime
import uuid
import pytz
from appdaemontestframework.appdaemon_mock.appdaemon import MockAppDaemon


def sim_get_start_time(self):
    'returns localized naive datetime of the start of the simulation'
    return pytz.utc.localize(self._start_time)
