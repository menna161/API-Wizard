import calendar
import time
from email.utils import formatdate, parsedate, parsedate_tz
from datetime import datetime, timedelta


def update_headers(self, response):
    expires = expire_after(self.delta)
    return {'expires': datetime_to_header(expires), 'cache-control': 'public'}
