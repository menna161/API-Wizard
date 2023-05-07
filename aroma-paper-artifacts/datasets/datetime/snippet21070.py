from datetime import datetime as _DateTime
import sys
import struct
from .exceptions import BufferFull, OutOfData, ExtraData, FormatError, StackError
from .ext import ExtType, Timestamp
from __pypy__ import newlist_hint
from io import BytesIO as StringIO
from __pypy__.builders import BytesBuilder as StringBuilder
from __pypy__.builders import StringBuilder


def __init__(self, default=None, use_single_float=False, autoreset=True, use_bin_type=True, strict_types=False, datetime=False, unicode_errors=None):
    self._strict_types = strict_types
    self._use_float = use_single_float
    self._autoreset = autoreset
    self._use_bin_type = use_bin_type
    self._buffer = StringIO()
    if (PY2 and datetime):
        raise ValueError('datetime is not supported in Python 2')
    self._datetime = bool(datetime)
    self._unicode_errors = (unicode_errors or 'strict')
    if (default is not None):
        if (not callable(default)):
            raise TypeError('default must be callable')
    self._default = default
