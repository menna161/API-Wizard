import datetime
import struct
from six.moves import winreg
from six import text_type
from ._common import tzname_in_python2
import ctypes
from ctypes import wintypes


def dst(self, dt):
    isdst = self._isdst(dt)
    if (isdst is None):
        return None
    elif isdst:
        minutes = (self._dstoffset - self._stdoffset)
        return datetime.timedelta(minutes=minutes)
    else:
        return datetime.timedelta(0)
