from collections import namedtuple
import datetime
import io
import math
import plistlib
from struct import pack, unpack, unpack_from
from struct import error as struct_error
import sys
import time


def writeObject(self, obj, output, setReferencePosition=False):
    'Serializes the given object to the output. Returns output.\n           If setReferencePosition is True, will set the position the\n           object was written.\n        '

    def proc_variable_length(format, length):
        result = b''
        if (length > 14):
            result += pack('!B', ((format << 4) | 15))
            result = self.writeObject(length, result)
        else:
            result += pack('!B', ((format << 4) | length))
        return result

    def timedelta_total_seconds(td):
        return ((td.microseconds + ((td.seconds + ((td.days * 24) * 3600)) * (10.0 ** 6))) / (10.0 ** 6))
    if setReferencePosition:
        self.referencePositions[obj] = len(output)
    if (obj is None):
        output += pack('!B', 0)
    elif isinstance(obj, BoolWrapper):
        if (obj.value is False):
            output += pack('!B', 8)
        else:
            output += pack('!B', 9)
    elif isinstance(obj, Uid):
        size = self.intSize(obj.integer)
        output += pack('!B', ((8 << 4) | (size - 1)))
        output += self.binaryInt(obj.integer)
    elif isinstance(obj, (int, long)):
        byteSize = self.intSize(obj)
        root = math.log(byteSize, 2)
        output += pack('!B', ((1 << 4) | int(root)))
        output += self.binaryInt(obj, as_number=True)
    elif isinstance(obj, FloatWrapper):
        output += pack('!B', ((2 << 4) | 3))
        output += self.binaryReal(obj)
    elif isinstance(obj, datetime.datetime):
        try:
            timestamp = (obj - apple_reference_date).total_seconds()
        except AttributeError:
            timestamp = timedelta_total_seconds((obj - apple_reference_date))
        output += pack('!B', 51)
        output += pack('!d', float(timestamp))
    elif isinstance(obj, Data):
        output += proc_variable_length(4, len(obj))
        output += obj
    elif isinstance(obj, StringWrapper):
        output += proc_variable_length(obj.encodingMarker, len(obj))
        output += obj.encodedValue
    elif isinstance(obj, bytes):
        output += proc_variable_length(5, len(obj))
        output += obj
    elif isinstance(obj, HashableWrapper):
        obj = obj.value
        if isinstance(obj, (set, list, tuple)):
            if isinstance(obj, set):
                output += proc_variable_length(12, len(obj))
            else:
                output += proc_variable_length(10, len(obj))
            objectsToWrite = []
            for objRef in obj:
                (isNew, output) = self.writeObjectReference(objRef, output)
                if isNew:
                    objectsToWrite.append(objRef)
            for objRef in objectsToWrite:
                output = self.writeObject(objRef, output, setReferencePosition=True)
        elif isinstance(obj, dict):
            output += proc_variable_length(13, len(obj))
            keys = []
            values = []
            objectsToWrite = []
            for (key, value) in iteritems(obj):
                keys.append(key)
                values.append(value)
            for key in keys:
                (isNew, output) = self.writeObjectReference(key, output)
                if isNew:
                    objectsToWrite.append(key)
            for value in values:
                (isNew, output) = self.writeObjectReference(value, output)
                if isNew:
                    objectsToWrite.append(value)
            for objRef in objectsToWrite:
                output = self.writeObject(objRef, output, setReferencePosition=True)
    return output
