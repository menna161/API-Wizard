import datetime
import uuid
import pytz
from appdaemontestframework.appdaemon_mock.appdaemon import MockAppDaemon


def sim_set_start_time(self, time):
    'Set the absolute start time and set current time to that as well.\n        if time is a datetime, it goes right to that.\n        if time is time, it will set to that time with the current date.\n        All dates/datetimes should be localized naive\n\n        To guarantee consistency, you can not set the start time while any callbacks are scheduled.\n        '
    if (len(self._registered_callbacks) > 0):
        raise RuntimeError('You can not set start time while callbacks are scheduled')
    if (type(time) == datetime.time):
        time = datetime.datetime.combine(self._now.date(), time)
    self._start_time = self._now = time
