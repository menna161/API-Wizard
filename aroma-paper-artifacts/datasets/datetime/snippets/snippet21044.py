from collections import namedtuple
import datetime
import sys
import struct


@staticmethod
def from_datetime(dt):
    'Create a Timestamp from datetime with tzinfo.\n\n        Python 2 is not supported.\n\n        :rtype: Timestamp\n        '
    return Timestamp.from_unix(dt.timestamp())
