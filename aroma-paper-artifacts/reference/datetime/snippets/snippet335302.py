import datetime
import uuid
import pytz
from appdaemontestframework.appdaemon_mock.appdaemon import MockAppDaemon


def sim_fast_forward(self, time):
    'Fastforward time and invoke callbacks. time can be a timedelta, time, or datetime (all should be localized naive)'
    if (type(time) == datetime.timedelta):
        target_datetime = (self._now + time)
    elif (type(time) == datetime.time):
        if (time > self._now.time()):
            target_datetime = datetime.datetime.combine(self._now.date(), time)
        else:
            target_date = (self._now.date() + datetime.timedelta(days=1))
            target_datetime = datetime.datetime.combine(target_date, time)
    elif (type(time) == datetime.datetime):
        target_datetime = time
    else:
        raise ValueError(f"Unknown time type '{type(time)}' for fast_forward")
    self._run_callbacks_and_advance_time(target_datetime)
