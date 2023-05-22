from collections import namedtuple
import datetime
import io
import math
import plistlib
from struct import pack, unpack, unpack_from
from struct import error as struct_error
import sys
import time


def computeOffsets(self, obj, asReference=False, isRoot=False):

    def check_key(key):
        if (key is None):
            raise InvalidPlistException('Dictionary keys cannot be null in plists.')
        elif isinstance(key, Data):
            raise InvalidPlistException('Data cannot be dictionary keys in plists.')
        elif (not isinstance(key, StringWrapper)):
            raise InvalidPlistException('Keys must be strings.')

    def proc_size(size):
        if (size > 14):
            size += self.intSize(size)
        return size
    if asReference:
        if (obj in self.computedUniques):
            return
        else:
            self.computedUniques.add(obj)
    if (obj is None):
        self.incrementByteCount('nullBytes')
    elif isinstance(obj, BoolWrapper):
        self.incrementByteCount('boolBytes')
    elif isinstance(obj, Uid):
        size = self.intSize(obj.integer)
        self.incrementByteCount('uidBytes', incr=(1 + size))
    elif isinstance(obj, (int, long)):
        size = self.intSize(obj)
        self.incrementByteCount('intBytes', incr=(1 + size))
    elif isinstance(obj, FloatWrapper):
        size = self.realSize(obj)
        self.incrementByteCount('realBytes', incr=(1 + size))
    elif isinstance(obj, datetime.datetime):
        self.incrementByteCount('dateBytes', incr=2)
    elif isinstance(obj, Data):
        size = proc_size(len(obj))
        self.incrementByteCount('dataBytes', incr=(1 + size))
    elif isinstance(obj, StringWrapper):
        size = proc_size(len(obj))
        self.incrementByteCount('stringBytes', incr=(1 + size))
    elif isinstance(obj, HashableWrapper):
        obj = obj.value
        if isinstance(obj, set):
            size = proc_size(len(obj))
            self.incrementByteCount('setBytes', incr=(1 + size))
            for value in obj:
                self.computeOffsets(value, asReference=True)
        elif isinstance(obj, (list, tuple)):
            size = proc_size(len(obj))
            self.incrementByteCount('arrayBytes', incr=(1 + size))
            for value in obj:
                asRef = True
                self.computeOffsets(value, asReference=True)
        elif isinstance(obj, dict):
            size = proc_size(len(obj))
            self.incrementByteCount('dictBytes', incr=(1 + size))
            for (key, value) in iteritems(obj):
                check_key(key)
                self.computeOffsets(key, asReference=True)
                self.computeOffsets(value, asReference=True)
    else:
        raise InvalidPlistException(('Unknown object type: %s (%s)' % (type(obj).__name__, repr(obj))))
