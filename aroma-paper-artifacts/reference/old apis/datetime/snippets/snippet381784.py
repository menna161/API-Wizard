import binascii
import datetime
from bitstring import BitArray


def decodeValue(data):
    dataType = data.read(8).int
    if (dataType == 0):
        return None
    elif (dataType == 1):
        if data.read(8).int:
            return True
        else:
            return False
    elif (dataType == 2):
        return data.read(32).int
    elif (dataType == 3):
        return data.read(64).int
    elif (dataType == 4):
        return data.read(64).float
    elif (dataType == 5):
        return decodeString(data)
    elif (dataType == 6):
        return decodeDictionary(data)
    elif (dataType == 7):
        return decodeArray(data)
    elif (dataType == 8):
        return datetime.datetime.fromtimestamp((data.read(64).int / 1000))
    else:
        raise ValueError(f'Wrong datatype: {dataType}')
