import logging
import traceback
from datetime import datetime
from sap.cf_logging import defaults
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.record import application_info
from sap.cf_logging.record import util
from sap.cf_logging.formatters.stacktrace_formatter import format_stacktrace


def __init__(self, extra, framework, *args, **kwargs):
    super(SimpleLogRecord, self).__init__(*args, **kwargs)
    utcnow = datetime.utcnow()
    self.written_at = util.iso_time_format(utcnow)
    self.written_ts = util.epoch_nano_second(utcnow)
    request = (extra[REQUEST_KEY] if (extra and (REQUEST_KEY in extra)) else None)
    self.correlation_id = (framework.context.get_correlation_id(request) or defaults.UNKNOWN)
    self.custom_fields = {}
    for (key, value) in framework.custom_fields.items():
        if (extra and (key in extra)):
            if (extra[key] is not None):
                self.custom_fields[key] = extra[key]
        elif (value is not None):
            self.custom_fields[key] = value
    self.extra = (dict(((key, value) for (key, value) in extra.items() if ((key not in _SKIP_ATTRIBUTES) and (key not in framework.custom_fields.keys())))) if extra else {})
    for (key, value) in self.extra.items():
        setattr(self, key, value)
