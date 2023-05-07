from collections import namedtuple
import datetime
import sys
import struct


def to_datetime(self):
    'Get the timestamp as a UTC datetime.\n\n        Python 2 is not supported.\n\n        :rtype: datetime.\n        '
    return datetime.datetime.fromtimestamp(self.to_unix(), _utc)
