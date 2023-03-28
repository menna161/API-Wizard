import datetime
import uuid
import pytz
from appdaemontestframework.appdaemon_mock.appdaemon import MockAppDaemon


def __init__(self, AD: MockAppDaemon):
    self.AD = AD
    self._registered_callbacks = []
    self.sim_set_start_time(datetime.datetime(2000, 1, 1, 0, 0))
