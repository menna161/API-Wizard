from collections import namedtuple
import datetime
import io
import math
import plistlib
from struct import pack, unpack, unpack_from
from struct import error as struct_error
import sys
import time


def readDate(self):
    result = unpack('>d', self.contents[self.currentOffset:(self.currentOffset + 8)])[0]
    result = (datetime.timedelta(seconds=result) + apple_reference_date)
    self.currentOffset += 8
    return result
