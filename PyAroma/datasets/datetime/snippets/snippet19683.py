import calendar
import time
from email.utils import formatdate, parsedate, parsedate_tz
from datetime import datetime, timedelta


def expire_after(delta, date=None):
    date = (date or datetime.utcnow())
    return (date + delta)
