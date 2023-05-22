from datetime import datetime, timedelta
import time


@property
def timestamp_second(self):
    '\n        时间戳(秒)\n        '
    return int(self._datetime.strftime('%s'))
