from appdaemontestframework.hass_mocks import HassMocks
import datetime


def _fast_forward_seconds(self, seconds_to_fast_forward):
    self._hass_mocks.AD.sched.sim_fast_forward(datetime.timedelta(seconds=seconds_to_fast_forward))
