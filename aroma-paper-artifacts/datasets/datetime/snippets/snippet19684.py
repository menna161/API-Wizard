import calendar
import time
from email.utils import formatdate, parsedate, parsedate_tz
from datetime import datetime, timedelta


def datetime_to_header(dt):
    return formatdate(calendar.timegm(dt.timetuple()))
