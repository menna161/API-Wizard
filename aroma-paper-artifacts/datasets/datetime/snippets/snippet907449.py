from datetime import datetime, timedelta
import time


def _parse_timestamp(self, time_object):
    '\n        解析时间戳\n        '
    if (len(str(int(time_object))) == 10):
        self._datetime = datetime.fromtimestamp(time_object)
    elif (len(str(int(time_object))) == 13):
        self._datetime = datetime.fromtimestamp((time_object / 1000.0))
    else:
        raise ValueError(u'输入的时间格式不正确')
