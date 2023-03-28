from workflow import Workflow3
from workflow.workflow3 import Item3
from settings import get_login, get_password, get_regex, get_server
import calendar
from datetime import datetime, timedelta
import logging
import logging.handlers
import os
import dateutil.parser
import pytz
import dateutil.parser
import pytz
import re


def utc_to_local(self, utc_dt):
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert (utc_dt.resolution >= timedelta(microseconds=1))
    return local_dt.replace(microsecond=utc_dt.microsecond)
