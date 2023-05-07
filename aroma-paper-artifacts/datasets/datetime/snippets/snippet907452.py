from datetime import datetime, timedelta
import time


@property
def timestamp_microsecond(self):
    '\n        时间戳(毫秒)\n        '
    return int(((time.mktime(self._datetime.timetuple()) * 1000.0) + (self._datetime.microsecond / 1000.0)))
