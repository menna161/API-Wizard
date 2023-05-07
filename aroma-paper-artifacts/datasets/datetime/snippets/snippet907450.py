from datetime import datetime, timedelta
import time


def _parse_time_str(self, time_object):
    '\n        解析时间字符串\n        '
    for i in datetime_formats:
        try:
            self._datetime = datetime.strptime(time_object, i)
            break
        except:
            continue
    if (not self._datetime):
        raise ValueError(u'输入的时间格式不正确')
