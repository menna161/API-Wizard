from datetime import datetime as _DateTime
import sys
import struct
from .exceptions import BufferFull, OutOfData, ExtraData, FormatError, StackError
from .ext import ExtType, Timestamp
from __pypy__ import newlist_hint
from io import BytesIO as StringIO
from __pypy__.builders import BytesBuilder as StringBuilder
from __pypy__.builders import StringBuilder


def _pack(self, obj, nest_limit=DEFAULT_RECURSE_LIMIT, check=isinstance, check_type_strict=_check_type_strict):
    default_used = False
    if self._strict_types:
        check = check_type_strict
        list_types = list
    else:
        list_types = (list, tuple)
    while True:
        if (nest_limit < 0):
            raise ValueError('recursion limit exceeded')
        if (obj is None):
            return self._buffer.write(b'\xc0')
        if check(obj, bool):
            if obj:
                return self._buffer.write(b'\xc3')
            return self._buffer.write(b'\xc2')
        if check(obj, int_types):
            if (0 <= obj < 128):
                return self._buffer.write(struct.pack('B', obj))
            if ((- 32) <= obj < 0):
                return self._buffer.write(struct.pack('b', obj))
            if (128 <= obj <= 255):
                return self._buffer.write(struct.pack('BB', 204, obj))
            if ((- 128) <= obj < 0):
                return self._buffer.write(struct.pack('>Bb', 208, obj))
            if (255 < obj <= 65535):
                return self._buffer.write(struct.pack('>BH', 205, obj))
            if ((- 32768) <= obj < (- 128)):
                return self._buffer.write(struct.pack('>Bh', 209, obj))
            if (65535 < obj <= 4294967295):
                return self._buffer.write(struct.pack('>BI', 206, obj))
            if ((- 2147483648) <= obj < (- 32768)):
                return self._buffer.write(struct.pack('>Bi', 210, obj))
            if (4294967295 < obj <= 18446744073709551615):
                return self._buffer.write(struct.pack('>BQ', 207, obj))
            if ((- 9223372036854775808) <= obj < (- 2147483648)):
                return self._buffer.write(struct.pack('>Bq', 211, obj))
            if ((not default_used) and (self._default is not None)):
                obj = self._default(obj)
                default_used = True
                continue
            raise OverflowError('Integer value out of range')
        if check(obj, (bytes, bytearray)):
            n = len(obj)
            if (n >= (2 ** 32)):
                raise ValueError(('%s is too large' % type(obj).__name__))
            self._pack_bin_header(n)
            return self._buffer.write(obj)
        if check(obj, unicode):
            obj = obj.encode('utf-8', self._unicode_errors)
            n = len(obj)
            if (n >= (2 ** 32)):
                raise ValueError('String is too large')
            self._pack_raw_header(n)
            return self._buffer.write(obj)
        if check(obj, memoryview):
            n = (len(obj) * obj.itemsize)
            if (n >= (2 ** 32)):
                raise ValueError('Memoryview is too large')
            self._pack_bin_header(n)
            return self._buffer.write(obj)
        if check(obj, float):
            if self._use_float:
                return self._buffer.write(struct.pack('>Bf', 202, obj))
            return self._buffer.write(struct.pack('>Bd', 203, obj))
        if check(obj, (ExtType, Timestamp)):
            if check(obj, Timestamp):
                code = (- 1)
                data = obj.to_bytes()
            else:
                code = obj.code
                data = obj.data
            assert isinstance(code, int)
            assert isinstance(data, bytes)
            L = len(data)
            if (L == 1):
                self._buffer.write(b'\xd4')
            elif (L == 2):
                self._buffer.write(b'\xd5')
            elif (L == 4):
                self._buffer.write(b'\xd6')
            elif (L == 8):
                self._buffer.write(b'\xd7')
            elif (L == 16):
                self._buffer.write(b'\xd8')
            elif (L <= 255):
                self._buffer.write(struct.pack('>BB', 199, L))
            elif (L <= 65535):
                self._buffer.write(struct.pack('>BH', 200, L))
            else:
                self._buffer.write(struct.pack('>BI', 201, L))
            self._buffer.write(struct.pack('b', code))
            self._buffer.write(data)
            return
        if check(obj, list_types):
            n = len(obj)
            self._pack_array_header(n)
            for i in xrange(n):
                self._pack(obj[i], (nest_limit - 1))
            return
        if check(obj, dict):
            return self._pack_map_pairs(len(obj), dict_iteritems(obj), (nest_limit - 1))
        if (self._datetime and check(obj, _DateTime)):
            obj = Timestamp.from_datetime(obj)
            default_used = 1
            continue
        if ((not default_used) and (self._default is not None)):
            obj = self._default(obj)
            default_used = 1
            continue
        raise TypeError(('Cannot serialize %r' % (obj,)))
