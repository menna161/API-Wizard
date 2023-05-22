import datetime
import uuid
import pytz
from appdaemontestframework.appdaemon_mock.appdaemon import MockAppDaemon


def _run_callbacks_and_advance_time(self, target_datetime, run_callbacks=True):
    'run all callbacks scheduled between now and target_datetime'
    if (target_datetime < self._now):
        raise ValueError('You can not fast forward to a time in the past.')
    while True:
        callbacks_to_run = [x for x in self._registered_callbacks if (x.run_date_time <= target_datetime)]
        if (not callbacks_to_run):
            break
        callbacks_to_run.sort(key=(lambda cb: cb.run_date_time))
        callback = callbacks_to_run[0]
        self._now = callback.run_date_time
        if run_callbacks:
            callback()
        if (callback.interval > 0):
            callback.run_date_time += datetime.timedelta(seconds=callback.interval)
        else:
            self._registered_callbacks.remove(callback)
    self._now = target_datetime
