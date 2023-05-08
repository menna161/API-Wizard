import datetime
import uuid
import pytz
from appdaemontestframework.appdaemon_mock.appdaemon import MockAppDaemon


def make_naive(self, dt):
    local = dt.astimezone(self.AD.tz)
    return datetime.datetime(local.year, local.month, local.day, local.hour, local.minute, local.second, local.microsecond)
