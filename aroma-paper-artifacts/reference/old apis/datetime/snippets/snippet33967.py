import datetime
import struct
from six.moves import winreg
from six import text_type
from ._common import tzname_in_python2
import ctypes
from ctypes import wintypes


def utcoffset(self, dt):
    isdst = self._isdst(dt)
    if (isdst is None):
        return None
    elif isdst:
        return datetime.timedelta(minutes=self._dstoffset)
    else:
        return datetime.timedelta(minutes=self._stdoffset)
