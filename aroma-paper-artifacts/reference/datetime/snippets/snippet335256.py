from datetime import datetime
from appdaemontestframework.common import AppdaemonTestFrameworkError
from appdaemontestframework.hass_mocks import HassMocks


def time_is(self, time_as_datetime):
    self._hass_mocks.AD.sched.sim_set_start_time(time_as_datetime)
