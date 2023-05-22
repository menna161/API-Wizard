from datetime import datetime, timedelta
import time


def sub(self, days=0, weeks=0, hours=0, minutes=0, seconds=0):
    '\n        减少时间\n        :param days: 天\n        :param weeks: 星期\n        :param hours: 小时\n        :param minutes: 分钟\n        :param seconds: 秒\n        :return: HumanDateTime对象\n        '
    return self.__class__(str((self._datetime + timedelta(days=(- days), weeks=(- weeks), hours=(- hours), minutes=(- minutes), seconds=(- seconds)))))
