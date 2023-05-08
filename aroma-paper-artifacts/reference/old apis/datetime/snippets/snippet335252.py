from datetime import datetime
from appdaemontestframework.common import AppdaemonTestFrameworkError
from appdaemontestframework.hass_mocks import HassMocks


def _init_mocked_states(self):
    self.mocked_states = {}

    def get_state_mock(entity_id=None, *, attribute=None):
        if (entity_id is None):
            resdict = dict()
            for entityid in self.mocked_states:
                state = self.mocked_states[entityid]
                resdict.update({entityid: {'state': state['main'], 'attributes': state['attributes']}})
            return resdict
        else:
            if (entity_id not in self.mocked_states):
                raise StateNotSetError(entity_id)
            state = self.mocked_states[entity_id]
            if (attribute is None):
                return state['main']
            elif (attribute == 'all'):

                def format_time(timestamp: datetime):
                    if (not timestamp):
                        return None
                    return timestamp.isoformat()
                return {'last_updated': format_time(state['last_updated']), 'last_changed': format_time(state['last_changed']), 'state': state['main'], 'attributes': state['attributes'], 'entity_id': entity_id}
            else:
                return state['attributes'].get(attribute)
    self._hass_mocks.hass_functions['get_state'].side_effect = get_state_mock

    def entity_exists_mock(entity_id):
        return (entity_id in self.mocked_states)
    self._hass_mocks.hass_functions['entity_exists'].side_effect = entity_exists_mock
