from datetime import datetime
from appdaemontestframework.common import AppdaemonTestFrameworkError
from appdaemontestframework.hass_mocks import HassMocks


def format_time(timestamp: datetime):
    if (not timestamp):
        return None
    return timestamp.isoformat()
