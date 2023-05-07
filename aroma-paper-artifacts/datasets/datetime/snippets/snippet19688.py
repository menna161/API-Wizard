import calendar
import time
from email.utils import formatdate, parsedate, parsedate_tz
from datetime import datetime, timedelta


def update_headers(self, response):
    headers = {}
    if ('expires' not in response.headers):
        date = parsedate(response.headers['date'])
        expires = expire_after(timedelta(days=1), date=datetime(*date[:6]))
        headers['expires'] = datetime_to_header(expires)
        headers['cache-control'] = 'public'
    return headers
