from datetime import datetime as _DateTime
import sys
import struct
from .exceptions import BufferFull, OutOfData, ExtraData, FormatError, StackError
from .ext import ExtType, Timestamp
from __pypy__ import newlist_hint
from io import BytesIO as StringIO
from __pypy__.builders import BytesBuilder as StringBuilder
from __pypy__.builders import StringBuilder


def _unpack(self, execute=EX_CONSTRUCT):
    (typ, n, obj) = self._read_header(execute)
    if (execute == EX_READ_ARRAY_HEADER):
        if (typ != TYPE_ARRAY):
            raise ValueError('Expected array')
        return n
    if (execute == EX_READ_MAP_HEADER):
        if (typ != TYPE_MAP):
            raise ValueError('Expected map')
        return n
    if (typ == TYPE_ARRAY):
        if (execute == EX_SKIP):
            for i in xrange(n):
                self._unpack(EX_SKIP)
            return
        ret = newlist_hint(n)
        for i in xrange(n):
            ret.append(self._unpack(EX_CONSTRUCT))
        if (self._list_hook is not None):
            ret = self._list_hook(ret)
        return (ret if self._use_list else tuple(ret))
    if (typ == TYPE_MAP):
        if (execute == EX_SKIP):
            for i in xrange(n):
                self._unpack(EX_SKIP)
                self._unpack(EX_SKIP)
            return
        if (self._object_pairs_hook is not None):
            ret = self._object_pairs_hook(((self._unpack(EX_CONSTRUCT), self._unpack(EX_CONSTRUCT)) for _ in xrange(n)))
        else:
            ret = {}
            for _ in xrange(n):
                key = self._unpack(EX_CONSTRUCT)
                if (self._strict_map_key and (type(key) not in (unicode, bytes))):
                    raise ValueError(('%s is not allowed for map key' % str(type(key))))
                if ((not PY2) and (type(key) is str)):
                    key = sys.intern(key)
                ret[key] = self._unpack(EX_CONSTRUCT)
            if (self._object_hook is not None):
                ret = self._object_hook(ret)
        return ret
    if (execute == EX_SKIP):
        return
    if (typ == TYPE_RAW):
        if self._raw:
            obj = bytes(obj)
        else:
            obj = obj.decode('utf_8', self._unicode_errors)
        return obj
    if (typ == TYPE_BIN):
        return bytes(obj)
    if (typ == TYPE_EXT):
        if (n == (- 1)):
            ts = Timestamp.from_bytes(bytes(obj))
            if (self._timestamp == 1):
                return ts.to_unix()
            elif (self._timestamp == 2):
                return ts.to_unix_nano()
            elif (self._timestamp == 3):
                return ts.to_datetime()
            else:
                return ts
        else:
            return self._ext_hook(n, bytes(obj))
    assert (typ == TYPE_IMMEDIATE)
    return obj
