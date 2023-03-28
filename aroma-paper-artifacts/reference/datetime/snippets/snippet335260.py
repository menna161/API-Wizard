from datetime import datetime
from appdaemontestframework.common import AppdaemonTestFrameworkError
from appdaemontestframework.hass_mocks import HassMocks


def is_set_to(self, state, attributes=None, last_updated: datetime=None, last_changed: datetime=None):
    if (not attributes):
        attributes = {}
    given_that_wrapper.mocked_states[entity_id] = {'main': state, 'attributes': attributes, 'last_updated': last_updated, 'last_changed': last_changed}
